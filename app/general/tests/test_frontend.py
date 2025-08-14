import contextlib
import os
import time

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.common.exceptions import MoveTargetOutOfBoundsException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TITLE_404 = "Error"

# Wait timeout in seconds
WAIT_TIMEOUT = 5

DESKTOP_DIMENSIONS = (1920, 1080)
MOBILE_DIMENSIONS = (375, 667)  # iPhone SE 2nd gen
DEFAULT_DIMENSIONS = DESKTOP_DIMENSIONS


@tag("selenium")
class TestFrontend(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = os.environ.get("BROWSER", "chrome").lower()
        cls.js_enabled = os.environ.get("JS_ENABLED", "js-enabled") == "js-enabled"

        print(f"Running Selenium tests on {cls.browser}.")
        print(f"JS is {'enabled' if cls.js_enabled else 'disabled'}.")

        if cls.browser == "chrome":
            from selenium.webdriver.chrome.webdriver import Options, WebDriver

            options = Options()
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

            if not cls.js_enabled:
                # Taken from https://stackoverflow.com/a/73961818
                prefs = dict()
                prefs["webkit.webprefs.javascript_enabled"] = False
                prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
                prefs["profile.default_content_setting_values.javascript"] = 2
                prefs["profile.managed_default_content_settings.javascript"] = 2
                options.add_experimental_option("prefs", prefs)
                options.add_argument("--disable-javascript")

        elif cls.browser == "firefox":
            from selenium.webdriver.firefox.webdriver import Options, WebDriver

            options = Options()
            options.add_argument("-headless")
            options.set_preference("javascript.enabled", cls.js_enabled)

        else:
            print("Unrecognised web browser. Exiting.")
            exit(1)

        cls._options = options
        cls._WebDriver = WebDriver
        super().setUpClass()

    def setUp(self):
        self.driver = self._WebDriver(options=self._options)
        self.driver.set_window_size(*DEFAULT_DIMENSIONS)
        self.driver.implicitly_wait(WAIT_TIMEOUT)

    def tearDown(self):
        self.driver.quit()

    def set_window_size(self, x, y):
        self.driver.set_window_size(x, y)
        print(
            f"Asked for window size {(x, y)}, got {tuple(self.driver.get_window_size().values())}"
        )
        self.print_viewport()

    @contextlib.contextmanager
    def mobile_window_size(self):
        try:
            self.set_window_size(*MOBILE_DIMENSIONS)
            yield
        finally:
            self.set_window_size(*DEFAULT_DIMENSIONS)

    def print_viewport(self):
        w = self.driver.execute_script("return document.documentElement.clientWidth")
        h = self.driver.execute_script("return document.documentElement.clientHeight")
        print(f"Viewport: ({w}, {h})")

    # Checks that JS is properly disabled if passed through env var, else check if enabled
    def test_js_enabled_or_disabled(self):
        self.driver.get(f"file://{settings.TESTING_DIR}/test_js.html")
        self.assertEqual(
            len(self.driver.find_elements(By.ID, "js-enabled")), 1 if self.js_enabled else 0
        )

    # A few bugs encountered when using browser history
    def test_history(self):
        with self.mobile_window_size():
            # TODO: bootstrap hamburger doesn't work without JS :-(
            if self.js_enabled:
                self.driver.get(self.live_server_url)
                menu_button = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
                menu = self.driver.find_element(By.ID, "navbarPills")
                self.assertFalse(menu.is_displayed())
                menu_button.click()
                self.wait_until_displayed(menu)
                # The menu animation could still move things down, resulting in
                # visible elements moving out of the view part after moving to
                # them. This was a source of shaky Firefox tests on GitHub.
                # Let's sleep for the length of the animation:
                time.sleep(0.35)
                language_link = self.driver.find_element(
                    By.XPATH,
                    '//header//a[@href="/languages/"]',
                )
                # Similar link further down on the page that would exhibit the
                # problems with repositioning mentioned above:
                # language_link = self.driver.find_element(By.XPATH, '//main//a[@href="/languages/"]')
                self.move_to(language_link)
                language_link.click()
                self.wait_for_title("Languages")
                self.driver.back()
                self.wait_for_title("LwimiLinks")
                menu_button = self.driver.find_element(By.CLASS_NAME, "navbar-toggler")
                menu = self.driver.find_element(By.ID, "navbarPills")
                self.move_to(menu_button)
                self.wait_until_displayed(menu)
                menu_button.click()
                self.wait_until_not_displayed(menu)

    def test_no_404s(self):
        # Sanity check in case we ever change the 404 title
        self.driver.get(f"{self.live_server_url}/blabla404")
        self.assertTrue(
            self.driver.title.startswith(TITLE_404),
            f"Actual title was {self.driver.title}. Page: {self.driver.page_source}",
        )

        # Check all nav items
        for item in ["Search", "Institutions", "Projects", "Documents", "Languages", "Subjects"]:
            self.check_nav_item(item)

        # These URLs are available without loging in. This basic test just
        # ensures that they load cleanly and the titles are updated in all
        # tested configurations.
        for url, title in [
            ("/", "LwimiLinks"),
            ("/about/", "LwimiLinks"),  # review title
            ("/accounts/register/", "Register"),
            ("/accounts/login/", "Log in"),
            ("/accounts/password_reset/", "Password reset"),
            ("/accounts/reset/done/", "Password reset complete"),
            ("/accounts/reset/x/x/", "Password reset unsuccessful"),
            ("/legal_notices/", "LwimiLinks"),  # review title
        ]:
            self.driver.get(f"{self.live_server_url}{url}")
            self.wait_for_page(title)

    def check_nav_item(self, link_text):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text).click()
        self.wait_for_page(link_text)

    def wait_for_title(self, text):
        if self.browser == "firefox":
            # Seem to stabilise some tests regardless of timeout below :-/
            time.sleep(0.35)
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.title_contains(text),
            f"Didn't see title `{text}`. Seeing `{self.driver.title}`",
        )

    def wait_until_displayed(self, element):
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.visibility_of(element),
            f"`{element.tag_name}#{element.get_attribute('id')}` didn't appear",
        )

    def wait_until_not_displayed(self, element):
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(
            EC.invisibility_of_element(element),
            f"`{element.tag_name}#{element.get_attribute('id')}` didn't hide",
        )

    def move_to(self, element):
        if self.browser == "firefox":
            # .move_to_element() doesn't seem to do what is needed on Firefox.
            # Common advice is a script like this:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            # Since scrolling (above) happens asynchronously, we have to wait
            # to be sure the scrolling is done:
            time.sleep(1)
        actions = ActionChains(self.driver)
        actions.scroll_to_element(element)
        actions.move_to_element(element)
        try:
            actions.perform()
        except MoveTargetOutOfBoundsException as e:
            print(e)
            self.print_viewport()
            print("Element information:", element.rect)
            print("Font:", element.value_of_css_property("font-size"))
            name = f"{id(element)}-{element.tag_name}"
            self.driver.save_screenshot(f"{settings.BASE_DIR}/selenium-screenshots/{name}.png")
            self.driver.save_full_page_screenshot(
                f"{settings.BASE_DIR}/selenium-screenshots/fs-{name}.png"
            )
            raise

    def wait_for_page(self, title, success=True):
        id_ = ""
        try:
            self.wait_for_title(title)
            self.assertFalse(
                self.driver.title.startswith("ProgrammingError"),
                f"Actual title was {self.driver.title}",
            )
            # Every page must have #main as it is our default htmx target
            id_ = "main"
            self.assertTrue(self.driver.find_element(By.ID, "main"))
            # Every page must have #main-heading, since it is referred to in the
            # `aria-labelledby` of the `main` tag. For now that is not yet in
            # place on error pages.
            if success:
                id_ = "main-heading"
                self.assertTrue(self.driver.find_element(By.ID, "main-heading"))
                assertion = self.wait_until_not_displayed
            else:
                assertion = self.wait_until_displayed
            id_ = "error-block"
            assertion(self.driver.find_element(By.ID, "error-block"))
        except NoSuchElementException as e:
            print(e)
            print(f"...while looking for id `{id_}`.")
            print(self.driver.page_source)
            raise
        except AssertionError as e:
            print(e)
            name = f"error-visibility-id={id_}"
            self.driver.save_screenshot(f"{settings.BASE_DIR}/selenium-screenshots/{name}.png")
            raise

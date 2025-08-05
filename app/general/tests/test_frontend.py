import contextlib
import os

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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

        print(
            f"Running Selenium tests on {cls.browser}. JS is {'enabled' if cls.js_enabled else 'disabled'}."
        )

        if cls.browser == "chrome":
            from selenium.webdriver.chrome.webdriver import Options, WebDriver

            opts = Options()
            opts.add_argument("--headless=new")
            opts.add_argument("--no-sandbox")
            opts.add_argument("--disable-dev-shm-usage")
            opts.add_argument("--window-size=1920,1080")

            if not cls.js_enabled:
                # Taken from https://stackoverflow.com/a/73961818
                prefs = dict()
                prefs["webkit.webprefs.javascript_enabled"] = False
                prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
                prefs["profile.default_content_setting_values.javascript"] = 2
                prefs["profile.managed_default_content_settings.javascript"] = 2
                opts.add_experimental_option("prefs", prefs)
                opts.add_argument("--disable-javascript")

            cls.driver = WebDriver(opts)
        elif cls.browser == "firefox":
            from selenium.webdriver.firefox.webdriver import Options, WebDriver

            options = Options()
            options.add_argument("-headless")
            options.set_preference("javascript.enabled", cls.js_enabled)
            cls.driver = WebDriver(options=options)

        cls.driver.set_window_size(*DEFAULT_DIMENSIONS)
        cls.driver.implicitly_wait(WAIT_TIMEOUT)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

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
        test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        self.driver.get(f"file://{test_dir}/test_js.html")
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
                language_link = self.driver.find_element(By.LINK_TEXT, "Languages")
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
            self.driver.title.startswith("Error"),
            f"Actual title was {self.driver.title}. Page: {self.driver.page_source}",
        )

        # Check main page does not 404
        self.driver.get(self.live_server_url)
        self.assert_current_page_not_error()

        # Check all nav items
        for item in ["Search", "Institutions", "Projects", "Documents", "Languages", "Subjects"]:
            self.check_nav_item(item)

    def check_nav_item(self, link_text):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text).click()

        # We use 'in' to do a more permissive match (for instance 'Search' is usually '<search query> - Search'
        self.wait_for_title(link_text)
        self.assert_current_page_not_error()

    def wait_for_title(self, text):
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(EC.title_contains(text))

    def wait_until_displayed(self, element):
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(EC.visibility_of(element))

    def wait_until_not_displayed(self, element):
        WebDriverWait(self.driver, WAIT_TIMEOUT).until(EC.invisibility_of_element(element))

    def move_to(self, element):
        # .move_to_element() doesn't seem to do what is needed on Firefox.
        # Common advice is a script like this:
        # self.driver.execute_script("arguments[0].scrollIntoView();", element)
        actions = ActionChains(self.driver)
        actions.scroll_to_element(element)
        actions.pause(0.1)  # Without some delay, element is not always (yet) in view
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

    def assert_current_page_not_error(self):
        self.assertFalse(
            self.driver.title.startswith("Error"), f"Actual title was {self.driver.title}"
        )
        self.assertFalse(
            self.driver.title.startswith("ProgrammingError"),
            f"Actual title was {self.driver.title}",
        )
        self.assertFalse(self.driver.find_element(By.ID, "error-block").is_displayed())

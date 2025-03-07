import contextlib
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
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
        browser = os.environ.get("BROWSER", "chrome").lower()
        cls.js_enabled = os.environ.get("JS_ENABLED", "js-enabled") == "js-enabled"

        print(
            f"Running Selenium tests on {browser}. JS is {'enabled' if cls.js_enabled else 'disabled'}."
        )

        if browser == "chrome":
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
        elif browser == "firefox":
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

    @classmethod
    @contextlib.contextmanager
    def mobile_window_size(cls):
        try:
            cls.driver.set_window_size(*MOBILE_DIMENSIONS)
            yield
        finally:
            cls.driver.set_window_size(*DEFAULT_DIMENSIONS)

    # Checks that JS is properly disabled if passed through env var, else check if enabled
    def test_js_enabled_or_disabled(self):
        test_dir = os.getenv("TESTING_DIR", "/app/general/tests/files")
        self.driver.get(f"file://{test_dir}/test_js.html")
        self.assertEqual(
            len(self.driver.find_elements(By.ID, "js-enabled")), 1 if self.js_enabled else 0
        )

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

    def assert_current_page_not_error(self):
        self.assertFalse(
            self.driver.title.startswith("Error"), f"Actual title was {self.driver.title}"
        )
        self.assertFalse(
            self.driver.title.startswith("ProgrammingError"),
            f"Actual title was {self.driver.title}",
        )
        self.assertFalse(self.driver.find_element(By.ID, "error-block").is_displayed())

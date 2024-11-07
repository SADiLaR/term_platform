import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import (
    Options as ChromeOptions,
)
from selenium.webdriver.chrome.webdriver import (
    WebDriver as ChromeWebDriver,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import (
    Options as FirefoxOptions,
)
from selenium.webdriver.firefox.webdriver import (
    WebDriver as FirefoxWebDriver,
)
from selenium.webdriver.support.wait import WebDriverWait

# Wait timeout in seconds
WAIT_TIMEOUT = 5


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
            opts = ChromeOptions()
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

            cls.driver = ChromeWebDriver(opts)
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("-headless")
            options.set_preference("javascript.enabled", cls.js_enabled)
            cls.driver = FirefoxWebDriver(options=options)

        cls.driver.implicitly_wait(WAIT_TIMEOUT)

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

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
        print(self.driver.title)
        assert self.driver.title.startswith(
            "Error"
        ), f"Actual title was {self.driver.title}. Page: {self.driver.page_source}"

        # Check main page does not 404
        self.driver.get(self.live_server_url)
        self.assert_current_page_not_error()

        # Check all nav items
        for item in ["Search", "Institutions", "Projects", "Documents", "Languages", "Subjects"]:
            self.check_nav_item(item)

    def check_nav_item(self, link_text):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, link_text).click()

        # We use 'in' to do a more permissive match (for instance 'Search' is usually '<search query> - Search'
        try:
            wait = WebDriverWait(self.driver, timeout=WAIT_TIMEOUT)
            wait.until(lambda d: link_text in self.driver.title)
        except TimeoutException:
            assert link_text in self.driver.title, (
                f"Expected title for page {link_text} to have {link_text};"
                f" was {self.driver.title}"
            )
        self.assert_current_page_not_error()

    def assert_current_page_not_error(self):
        assert not self.driver.title.startswith("Error"), f"Actual title was {self.driver.title}"
        assert not self.driver.title.startswith(
            "ProgrammingError"
        ), f"Actual title was {self.driver.title}"
        assert not self.driver.find_element(By.ID, "error-block").is_displayed()

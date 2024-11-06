from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import Options, WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Wait timeout in seconds
WAIT_TIMEOUT = 5


@tag("selenium")
class TestFrontend(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1920,1080")
        cls.driver = WebDriver(opts)
        cls.driver.implicitly_wait(WAIT_TIMEOUT)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

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

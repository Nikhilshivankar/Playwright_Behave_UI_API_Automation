from playwright.sync_api import Page
from utils.logger import logger
from config.settings import settings

class BasePage:
    """
    BasePage is a parent class for all Page Objects in the framework.
    It encapsulates the Playwright Page instance and provides resilient wrapper
    methods for common browser actions with automatic logging and configuration.
    """
    def __init__(self, page: Page):
        self.page = page
        self.timeout = settings.DEFAULT_TIMEOUT

    def navigate(self, path: str = ""):
        """Navigates the browser to the full URL composed of BASE_URL + path."""
        url = f"{settings.BASE_URL}{path}"
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url, timeout=self.timeout)

    def click(self, selector: str, description: str = ""):
        """Clicks an element defined by selector, with automated logging."""
        element_desc = description or selector
        logger.info(f"Clicking on element: '{element_desc}'")
        locator = self.page.locator(selector)
        locator.click(timeout=self.timeout)

    def fill(self, selector: str, value: str, description: str = "", is_secret: bool = False):
        """Fills an input field with the specified value. Masks the logged value if is_secret=True."""
        element_desc = description or selector
        logged_value = "********" if is_secret else value
        logger.info(f"Entering value into '{element_desc}': {logged_value}")
        locator = self.page.locator(selector)
        locator.fill(value, timeout=self.timeout)

    def get_text(self, selector: str) -> str:
        """Retrieves and returns the text content of the element matching the selector."""
        locator = self.page.locator(selector)
        text = locator.text_content(timeout=self.timeout) or ""
        text_stripped = text.strip()
        logger.debug(f"Retrieved text '{text_stripped}' from element '{selector}'")
        return text_stripped

    def is_visible(self, selector: str) -> bool:
        """Checks if the element matching the selector is visible."""
        visible = self.page.locator(selector).is_visible()
        logger.debug(f"Checking visibility of element '{selector}': {visible}")
        return visible

    def wait_for_element(self, selector: str, state: str = "visible"):
        """Waits for an element to reach a specific state ('attached', 'detached', 'visible', 'hidden')."""
        logger.debug(f"Waiting for element '{selector}' to be {state}")
        self.page.locator(selector).wait_for(state=state, timeout=self.timeout)

    def get_title(self) -> str:
        """Retrieves and returns the current browser window title."""
        title = self.page.title()
        logger.debug(f"Current page title is: '{title}'")
        return title

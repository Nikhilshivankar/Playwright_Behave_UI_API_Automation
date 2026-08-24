from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    LoginPage represents the Page Object Model (POM) for the Practice Test Login site.
    It contains element locators and action flows to authenticate and verify logins.
    """
    # UI Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON = "#submit"
    ERROR_MESSAGE = "#error"
    SUCCESS_HEADER = "h1.post-title"
    LOGOUT_BUTTON = "a:has-text('Log out')"

    def navigate_to_login(self):
        """Navigates to the practice login page."""
        self.navigate("/practice-test-login/")
        self.wait_for_element(self.USERNAME_INPUT)

    def login(self, username, password):
        """Executes the login workflow by filling the credentials and clicking submit."""
        self.fill(self.USERNAME_INPUT, username, description="Username Input")
        self.fill(self.PASSWORD_INPUT, password, description="Password Input", is_secret=True)
        self.click(self.SUBMIT_BUTTON, description="Submit Button")

    def get_error_message(self) -> str:
        """Retrieves validation or authentication error message content."""
        self.wait_for_element(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)

    def is_success_header_displayed(self) -> bool:
        """Checks if the successful login header is visible."""
        self.wait_for_element(self.SUCCESS_HEADER)
        return self.is_visible(self.SUCCESS_HEADER)

    def get_success_message_text(self) -> str:
        """Retrieves success header text after successful login."""
        return self.get_text(self.SUCCESS_HEADER)

    def is_logout_button_displayed(self) -> bool:
        """Checks if the Log Out button is visible on the dashboard."""
        return self.is_visible(self.LOGOUT_BUTTON)

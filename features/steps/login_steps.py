from behave import given, when, then
from config.settings import settings
import json
from pathlib import Path

# Load test data
TEST_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "test_data.json"
with open(TEST_DATA_PATH, "r", encoding="utf-8") as file:
    test_data = json.load(file)

@given("I navigate to the login page")
def step_navigate_to_login(context):
    context.login_page.navigate_to_login()

@when("I submit username and password")
def step_submit_valid_login(context):
    context.login_page.login(settings.TEST_USERNAME, settings.TEST_PASSWORD)

@when('I submit username "{username}" and password "{password}"')
def step_submit_invalid_login(context, username, password):
    context.login_page.login(username, password)

@then("I should see the login success message")
def step_verify_success_header(context):
    assert context.login_page.is_success_header_displayed(), "Success header not visible"
    header_text = context.login_page.get_success_message_text()
    expected = test_data["validation_messages"]["success_login_message"]
    assert expected in header_text, f"Expected '{expected}' inside '{header_text}'"

@then("the logout option should be visible")
def step_verify_logout_button(context):
    assert context.login_page.is_logout_button_displayed(), "Logout button not visible"

@then('I should see the error message "{expected_error}"')
def step_verify_error_message(context, expected_error):
    error_msg = context.login_page.get_error_message()
    assert expected_error in error_msg, f"Expected '{expected_error}' inside '{error_msg}'"

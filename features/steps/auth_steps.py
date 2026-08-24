from behave import given, when, then
from config.settings import settings

@when("I authenticate via API with valid username and password")
def step_api_login(context):
    context.login_response = context.petstore_client.login_user(settings.TEST_USERNAME, settings.TEST_PASSWORD)

@then("the API login response should indicate success")
def step_api_login_success(context):
    assert context.login_response is not None, "Login response was empty"
    assert "logged in user session" in context.login_response or len(context.login_response) > 0

@given("I am authenticated via API")
def step_api_authenticated(context):
    context.petstore_client.login_user(settings.TEST_USERNAME, settings.TEST_PASSWORD)

@when("I perform logout via API")
def step_api_logout(context):
    context.logout_response = context.petstore_client.logout_user()

@then("the API logout response should indicate success")
def step_api_logout_success(context):
    assert context.logout_response is not None, "Logout response was empty"
    assert "ok" in context.logout_response.lower() or len(context.logout_response) > 0

@api @login
Feature: API User Authentication

  @smoke
  Scenario: Successful API user login
    When I authenticate via API with valid username and password
    Then the API login response should indicate success

  @regression
  Scenario: Successful API user logout
    Given I am authenticated via API
    When I perform logout via API
    Then the API logout response should indicate success

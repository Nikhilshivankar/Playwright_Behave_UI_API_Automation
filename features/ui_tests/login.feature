@ui @login
Feature: UI User Authentication

  @smoke
  Scenario: Successful login with valid credentials
    Given I navigate to the login page
    When I submit username and password
    Then I should see the login success message
    And the logout option should be visible

  @regression
  Scenario Outline: Unsuccessful login with invalid credentials
    Given I navigate to the login page
    When I submit username "<username>" and password "<password>"
    Then I should see the error message "<expected_error>"

    Examples:
      | username      | password          | expected_error             |
      | incorrectUser | Password123       | Your username is invalid!  |
      | student       | incorrectPassword | Your password is invalid!  |


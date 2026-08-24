@api @pet
Feature: Pet CRUD Operations and Database Validation

  @smoke
  Scenario: Add a new pet and retrieve it by ID
    Given I prepare a request to add a new pet
    When I send the add pet API request
    Then the API response should contain the pet details
    And I should be able to fetch the pet by ID via API
    And the fetched pet details should match the created pet

  @regression
  Scenario: Update status of an existing pet
    Given I have created a pet with status "available"
    When I update the pet status to "sold" via API
    Then the pet status should be updated to "sold"
    And the pet should be found in the sold list

  @regression @database
  Scenario: Synchronize pet details with local database
    Given I have created a pet via API
    When I mirror the pet record in the local database
    Then the pet details in the database should match the API response

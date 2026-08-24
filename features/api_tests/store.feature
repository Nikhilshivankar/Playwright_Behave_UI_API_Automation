@api @store
Feature: Store Purchase Orders and Database Verification

  @regression @database
  Scenario: Place a pet purchase order, mirror in database, and delete it
    Given I place an order for pet ID 999 with quantity 2
    When I mirror the order record in the local database
    Then the order in the database should match the order API response
    And I should be able to fetch the order details via API
    And I delete the order via API
    And the local database order record should be cleaned up

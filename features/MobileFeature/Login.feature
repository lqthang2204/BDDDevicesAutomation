@test
Feature: navigate URL
  Scenario: test login page
    Given I navigate to url have index 1
    And I change the page spec to pageGoogle
    And I click element welcome-chrome
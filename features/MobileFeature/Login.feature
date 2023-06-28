@test
Feature: navigate URL
  Scenario: test login page
    Given I navigate to url have index 1
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I click element login-button
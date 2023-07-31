@parallel @web
Feature: test web page techpanda web

  Background: Test Background here
    Given I navigate to url TECHPANDA
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED

  @mc-guru6
  Scenario Outline: test Search function
    And I click element <product>
    And I type "test " into element search-input
    And I wait 5 seconds
    Examples:
      | product       |
      | mobile-button |
      | tv-button     |

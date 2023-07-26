@parallel @web
Feature: test web page techpanda web

  @mc-guru6
  Scenario Outline: test Search function
    Given I navigate to url have index 3
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I click element <product>
    And I type "test " into element search-input
    And I wait 5 seconds
    Examples:
      | product       |
      | mobile-button |
      | tv-button     |
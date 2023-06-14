@parallel
Feature: test web page techpanda
@mc-guru6
  Scenario Outline: test Search function
    Given I navigate to "http://live.techpanda.org/index.php/"
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I click element <product>
    And I type "test " into element search-input
    And I wait 5 seconds

    Examples:
      | product        |
      | mobile-button  |
      | tv-button  |
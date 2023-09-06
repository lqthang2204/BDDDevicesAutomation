@parallel @web @shadow
Feature: test web page techpanda web

  @mc-chrome-shadow
  Scenario: test shadow feature function
    Given I navigate to url CHROME-SETTING
    And I change the page spec to settingpage
    And I click element import borkmarks as shadow element
#    And I wait for element mobile-button to be DISPLAYED
#    And I click element <product>
#    And I type "test " into element search-input
#    And I wait 2 seconds
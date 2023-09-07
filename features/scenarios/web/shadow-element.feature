@parallel @web @shadow
Feature: test shadow elements

  @mc-chrome-shadow
  Scenario: test shadow feature function
    Given I navigate to url CHROME-SETTING
    And I change the page spec to settingpage
    And I click shadow element import borkmarks
    And I click shadow element import button
    And I wait 5 seconds
    And I click shadow element toogle button
    And I wait 5 seconds

    @mc-chrome-shadow-2
  Scenario: test shadow feature function
    Given I navigate to url CHROME-SETTING
    And I change the page spec to settingpage
    And I click shadow element search field
    And I type "Customize your Chrome profile" into shadow element search field
    And I wait 5 seconds
    And I clear shadow element search field
    And I wait 5 seconds
    And I click shadow element import borkmarks
    And I click shadow element import button
    And I wait 5 seconds

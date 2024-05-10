@web @regression @drag-drop
Feature: test feature drag and drop

  @drag-drop-1
  Scenario: test drag and drop 1
    Given I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
    And I drag and drop element bank_label to element debit_side
    And I wait 5 seconds

#  @drag-drop-2
#  Scenario: test drag and drop 2
#    Given I navigate to url GLOBAL_SQA
#    And I change the page spec to drag_global
#    And I wait for element image with text "High Tatras" to be DISPLAYED
#    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
#    And I drag and drop element bank_label to element debit_side
#    And I wait 5 seconds

  @scroll-to-element-1
  Scenario: test scroll to element
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
    And I verify that following elements with below attributes
      | Field                  | Value  | Status    | Helpers |
      | header-python-tutorial | Python | DISPLAYED |         |
    And I wait 10 seconds

  @scroll-to-element-2
  Scenario: test scroll to element 2
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
    And I scroll by java-script to element header-python-tutorial
    And I wait 10 seconds
    And I scroll to element python-tutorial with text "Execute Python"
    And I wait 10 seconds
    And I scroll to element header-python-tutorial
    And I wait 10 seconds

  @right-and-double-click
  Scenario: action right and double cliclk
    Given I navigate to url GURU99-DOUBLE
    And I change the page spec to double-example
    And I wait for element double-button to be ENABLED
    And I double-click element double-button
    And I accept for popup
    And I double-click element double-button
    And I dismiss for popup
    And I right-click element right-button
    And I wait for element edit-button to be DISPLAYED

  @switch-Iframe @norun
  Scenario: switch-Iframe
    Given I navigate to url GURU99-DOUBLE with options below
      | options   | value                       |
      | extension | AdBlock-best-ad-blocker.crx |
    And I wait 5 seconds
    And I switch active tab with title "AdBlock is now installed!"
    And I wait 20 seconds
#    And I close the tab with title "AdBlock is now installed!"
    And I close the tab with index 2
    And I switch active tab with title "Simple Context Menu"
    And I navigate to refresh-page
    And I change the page spec to double-example
    And I click element selenium-button
    And I wait for element selenium-demo-page to be ENABLED
    And I click element selenium-demo-page
#    And I switch to Iframe iframe-google-ads
#    And I perform click-if-exist-button action
#    And I switch Iframe default
    And I switch to Iframe iframe-topic
    And I wait 5 seconds
    And I wait for element banner-jmeter to be ENABLED
    And I scroll to element banner-jmeter
    And I click element banner-jmeter
    And I switch active tab with index 2
    And I switch active tab with title "Selenium Live Project: FREE Real Time Project for Practice"
    And I change the page spec to Selenium_Live_Project
    And I verify that following elements with below attributes
      | Field        | Value                                                      | Status    | Helpers |
      | title_header | Selenium Live Project: FREE Real Time Project for Practice | DISPLAYED |         |
    And I wait 5 seconds

@switch-Iframe-2 @norun
  Scenario: switch-Iframe drag
    Given I navigate to url GURU99-DOUBLE with options below
      | options   | value                       |
      | extension | AdBlock-best-ad-blocker.crx |
    And I wait 5 seconds
    And I switch active tab with title "AdBlock is now installed!"
    And I wait 10 seconds
    And I navigate to refresh-page
    And I switch active tab with title "Simple Context Menu"
    And I change the page spec to double-example
    And I click element selenium-button
    And I wait for element selenium-demo-page to be ENABLED
    And I click element selenium-demo-page
    And I switch to Iframe iframe-google-ads
#    And I perform click-if-exist-button action
#    And I switch Iframe default
#    And I switch to Iframe iframe-topic
#    And I wait 5 seconds
#    And I wait for element banner-jmeter to be ENABLED
#    And I scroll to element banner-jmeter
#    And I click element banner-jmeter
#    And I switch active tab with index 2
#    And I switch active tab with title "Selenium Live Project: FREE Real Time Project for Practice"
#    And I change the page spec to Selenium_Live_Project
#    And I verify that following elements with below attributes
#      | Field        | Value                                                      | Status    | Helpers |
#      | title_header | Selenium Live Project: FREE Real Time Project for Practice | DISPLAYED |         |
#    And I wait 5 seconds







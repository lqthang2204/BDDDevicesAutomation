@test-app-clock @mobile @ios
Feature:  mobile ios

  @safari_drag_and_drop
  Scenario: run safari to test drag and drop feature
    Given I change the page spec to mobile-drag-drop
    And I navigate to url CODESANDBOX
    And I wait for element click-run-button to be ENABLED
    And I click element click-run-button
    And I wait for element 1a-button to be DISPLAYED
    And I hover-over element 1a-button
   And I drag and drop element 1a-button to element 2a-button
#    And I click element continue-button
#    And I wait for element continue-button-pageÏ-2 to be ENABLED
#    And I click element continue-button-page-2
#    And I change the page spec to detail_health_page
#    And I verify that following elements with below attributes

  @click-ios
  Scenario: switch-Iframe
    Given I navigate to url GURU99-DOUBLE
    And I change the page spec to double-example
    And I click element selenium-button
    And I click element selenium-demo-page

  @scroll_element_ios
  Scenario: Scroll element demo IOS
    Given I change the page spec to indexRN
     And I click element username
     And I type "standard_user" into element username
     And I type "secret_sauce" into element password
     And I wait for element login-button to be ENABLED
     And I click element login-button
    And I wait for element product-one to be ENABLED
    And I click element product-one
    And I verify that following elements with below attributes
      | Field              | Value               | Status    | Helpers |
      | name-product       | Sauce Labs Backpack | DISPLAYED |         |
#      | Add-to-card-button | ADD TO CART         | ENABLED   |         |
     And I wait for element Back-button to be ENABLED
    And I click element Back-button
     And I wait 5 seconds
    And I scroll down to element product-six
    And I click element product-six
     And I wait for element Back-button to be ENABLED
    And I click element Back-button
     And I wait 5 seconds
#     And I scroll up to element product-two
    And I scroll up to element product-one
    And I click element product-one
#    And I click element product-six
#    //XCUIElementTypeStaticText[@name="Sauce Labs Backpack"]
#    And I click element selenium-button
#    And I click element selenium-demo-page
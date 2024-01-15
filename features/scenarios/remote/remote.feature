@remote
Feature:  test feature remote in saucelab

   @remote-android
  Scenario: Scroll element demo android
     Given I open application with config below
       | file config                            |
       | capabilities_android_app_demo_saucelab |
    And I change the page spec to indexRN
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

  @remote-ios
  Scenario: Scroll element demo IOS
    Given I open application with config below
      | file config                        |
      | capabilities_iOS_app_demo_saucelab |
    And I change the page spec to indexRN
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

  @remote-web
    Scenario: test drag and drop 1
    Given I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
    And I drag and drop element bank_label to element debit_side
    And I wait 5 seconds

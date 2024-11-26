@test @mobile @login_mobile
Feature: login mobile

  @login_android
  Scenario: test login page2 mobile
    Given I open application with config below
          | file config |
          | capabilities_android_chrome            |
    And I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I click element login-button

 @switch-Iframe-android
  Scenario: switch-Iframe
   Given I open application with config below
          | file config |
          | capabilities_android_chrome            |
    And I navigate to url GURU99-DOUBLE
    And I change the page spec to double-example
#   And I wait for element selenium-button to be ENABLED
    And I click element selenium-button
#    And I wait for element selenium-demo-page to be ENABLED
#   And I wait for element selenium-demo-page to be ENABLED
    And I click element selenium-demo-page
#    And I perform click-if-exist-button action
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

   @scroll_element_android
  Scenario: Scroll element demo android
     Given I open application with config below
          | file config |
          | capabilities_android_app_demo            |
    And I change the page spec to indexRN
     And I wait for element username to be ENABLED
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
  And I wait for element menu-bar to be ENABLED
  And I click element menu-bar
     And I change the page spec to MenuPage
  And I perform verify-menu action
  And I click element all-items
     And I change the page spec to indexRN
    And I wait for element product-one to be ENABLED
#    And I click element product-one
     And I save text for element price-for-pr1 with key "price1"
     And I wait for element add-to-card-pr1 to be ENABLED
  And I click element add-to-card-pr1
     And I wait for element add-to-card-pr1 to be ENABLED
  And I click element cart-button
  And I wait for element total-price to be DISPLAYED
  And I verify that following elements with below attributes
    | Field           | Value             | Status    | Helpers |
    | total-price     | KEY.price1        | DISPLAYED |         |
    | remove-button   | REMOVE            | ENABLED   |         |
    | continue-button | CONTINUE SHOPPING | ENABLED   |         |
    | checkout-button | CHECKOUT          | ENABLED   |         |

#    And I click element product-six
#    //XCUIElementTypeStaticText[@name="Sauce Labs Backpack"]
#    And I click element selenium-button
#    And I click element selenium-demo-page
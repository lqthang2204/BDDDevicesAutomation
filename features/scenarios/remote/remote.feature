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
  Scenario: test feature verify for elements
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage-Variant
    And I create a random user
    And I verify that following elements with below attributes
        | Field                     | Value           | Status    | Helpers          |
        | user-field                |                 | DISPLAYED |                  |
        | pass-field                |                 | DISPLAYED |                  |
    And I type "USER.first_name" into element user-field
    And I verify that following elements with below attributes
        | Field      | Value           | Status    | Helpers |
        | user-field | USER.first_name | DISPLAYED |         |
    And I clear text from element user-field
    And I wait for element location-option-inpatient to be ENABLED
    And I click element location-option-inpatient
    And I verify that following elements with below attributes
      | Field                     | Value                       | Status    | Helpers          |
      | user-field                |                             | DISPLAYED |                  |
      | pass-field                |                             | DISPLAYED |                  |
      | location-option-inpatient | Inpatient Ward              | DISPLAYED |                  |
      | location-option-inpatient | In                          | DISPLAYED | CONTAINS         |
      | location-option-inpatient | #007FFF                     | DISPLAYED | BACKGROUND-COLOR |
      | location-option-inpatient | #FFFFFF                     | DISPLAYED | COLOR            |
      | login-button              | #88af28                     | ENABLED   | BACKGROUND-COLOR |
      | login-button              | #FFFFFF                     | ENABLED   | COLOR            |
      | location-option-inpatient | Inpatient                   | DISPLAYED | STARTS_WITH      |
      | location-option-inpatient | Inpatient [A-z]             | DISPLAYED | REGEX            |
      | location-option-inpatient | Ward                        | DISPLAYED | ENDS_WITH        |
      | location-option-inpatient | OpenSans, Arial, sans-serif | DISPLAYED | FONT_FAMILY      |
      | location-option-inpatient | 16px                        | DISPLAYED | FONT_SIZE        |
      | location-option-inpatient | 400                         | DISPLAYED | FONT_WEIGHT      |
      | location-option-inpatient | 35px                        | DISPLAYED | FONT_HEIGHT      |
      | location-option-inpatient | left                        | DISPLAYED | TEXT_ALIGN       |
      | location-option-inpatient | 6                           | DISPLAYED | value            |
      | location-option-inpatient | 0                           | DISPLAYED | data-key         |
      | location-option-inpatient | selected                    | DISPLAYED | class            |

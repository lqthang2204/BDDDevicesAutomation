@regression @web @autoretry @norun
Feature: orange HRM 2 web

#  @Windows10_Chrome_76.0
#  @Windows10_Firefox_68.0
  @test-navigate-2-times
  Scenario: negative to url2
    Given I navigate to url GOOGLE
    And I change the page spec to pageGoogle
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I type "lqthang" into element search-field
    And I navigate to url TECHPANDA
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I wait for element mobile-button to be ENABLED
    And I wait for element mobile-button to be EXISTED
    And I click element mobile-button
    And I type "test" into element search-input

#  Scenario: This will not be included
#    Given I navigate to url have index 1
#    And I change the page spec to LoginPage
#    And I wait for element user-field to be DISPLAYED
#    And I wait for element pass-field to be DISPLAYED
#    And I type "Admin" into element user-field

  @web
  Scenario: test login page2
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I perform login-page action
    And I change the page spec to IndexPage
#    And I wait for element welcome-user to be DISPLAYED
#    And I wait for element log-out to be DISPLAYED

#  Scenario: This is commented script
#    Given I navigate to url have index 1
#    And I change the page spec to LoginPage
#    And I wait for element user-field to be DISPLAYED
#    And I wait for element pass-field to be DISPLAYED
#    And I type "Admin" into element user-field

  @web
  Scenario: This should not be included
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field

  @keyboard-1
  Scenario: execute keyboard with element
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I click keyboard NUMPAD1 button on element user-field
    And I wait 50 seconds

  @keyboard-2
  Scenario: execute keyboard without element keyboard
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I execute KEY_DOWN with keyboard CONTROL+a
    And I execute KEY_DOWN with keyboard CONTROL+c
    And I click element pass-field
    And I execute KEY_DOWN with keyboard CONTROL+v
    And I verify that following elements with below attributes
      | Field      | Value | Status    | Helpers |
      | pass-field | Admin | DISPLAYED |         |
    And I save text for element form-login with key "expect"
    And I verify that following elements with below attributes
      | Field      | Value             | Status    | Helpers  |
      | form-login | Inpatient Ward    | DISPLAYED | CONTAINS |
      | form-login | Isolation Ward    | DISPLAYED | CONTAINS |
      | form-login | Laboratory        | DISPLAYED | CONTAINS |
      | form-login | Outpatient Clinic | DISPLAYED | CONTAINS |
      | form-login | Pharmacy          | DISPLAYED | CONTAINS |
      | form-login | Registration Desk | DISPLAYED | CONTAINS |
      | form-login | Can't log in?     | DISPLAYED | CONTAINS |
    And I verify that following elements with below attributes
      | Field      | Value      | Status    | Helpers  |
      | form-login | KEY.expect | DISPLAYED | CONTAINS |

  @function-read-javascript
  Scenario: read javascript
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I wait for element location-option-inpatient to be ENABLED
    And I click element location-option-inpatient
    And I perform javascript isPageLoaded
    And I perform javascript elementIsOnScreen on element login-button
    And I perform javascript highlight on element login-button
    And I perform javascript clickElement on element login-button
    And I perform javascript isPageLoaded
    And I wait 50 seconds

  @test-javascript-auto-accept
  Scenario: switch-Iframe  test-javascript-auto-accept
    Given I navigate to url GURU99-DELETE
    And I change the page spec to delelePage
    And I click element customer-id
    And I perform javascript borderElement on element customer-id
    And I perform javascript highlight on element customer-id
    And I type "test" into element customer-id
    And I wait for element submit-button to be ENABLED
    And I click element submit-button
    And I wait 5 seconds
#    And I perform javascript isPageLoaded
#    And I perform javascript autoAcceptAlerts
    And I accept for popup
    And I wait 10 seconds

  @function-read-javascript-2
  Scenario: function-read-javascript-2
    Given I navigate to url GURU99-DOUBLE with options below
      | options   | value                       |
      | extension | AdBlock-best-ad-blocker.crx |
    And I wait 20 seconds
    And I switch active tab with title "AdBlock is now installed!"
    And I wait 10 seconds
#    And I close the tab with title "AdBlock is now installed!"
    And I close the tab with index 2
    And I switch active tab with title "Simple Context Menu"
    And I navigate to refresh-page
    And I change the page spec to checkBoxPage
    And I wait for element option-button with text "Selenium" to be ENABLED
    And I click element option-button with text "Selenium"
    And I wait for element option-button with text "Radio & Checkbox Demo" to be ENABLED
    And I click element option-button with text "Radio & Checkbox Demo"
    And I wait for element radio-one to be DISPLAYED
    And I click element radio-one
    And I perform javascript getCheckBxState on element radio-one

  @javascript-mouse-hover
  Scenario: test javascript function
    And I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
#    And I drag and drop element bank_label to element debit_side
    And I perform javascript mouseHover on element bank_label
#         And I perform javascript mouseHover on element debit_side
    And I perform javascript openNewTab
    And I switch active tab with index 2
    And I navigate to url GURU99
    And I perform javascript scrollToBottom
    And I perform javascript scrollToTop
    And I wait 5 seconds

  @scroll-to-element-3
  Scenario: test scroll to element 4
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
    And I wait for element header-python-tutorial to be DISPLAYED
#    And I scroll by java-script to element header-python-tutorial
    And I wait 10 seconds
    And I perform javascript scrollToElement with below arguments
      | arguments              |
      | title-page             |
      | header-python-tutorial |
    And I wait 5 seconds
    And I perform javascript scrollToElement with below arguments
      | arguments  |
      | title-page |
    And I wait 5 seconds


      @test-failed-rerun
  Scenario: test scroll to element 2
    Given I navigate to url INDEX_GURU
    And I change the page spec to index_guru
#    And I scroll by java-script to element header-python-tutorial
#    And I wait 10 seconds
    And I perform javascript scrollToElement with below arguments
      | arguments              |
      | title-page             |
      | header-python-tutorial |
    And I wait 5 seconds
    And I perform javascript scrollToElement with below arguments
      | arguments              |
      | header-python-tutorial |
      | title-page             |
        And I wait 5 seconds

    
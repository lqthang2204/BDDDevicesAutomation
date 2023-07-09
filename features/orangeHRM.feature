@regression @web
Feature: orange HRM web
#  @Windows10_Chrome_76.0
#  @Windows10_Firefox_68.0
  Scenario: negative to url
    Given I navigate to url have index 2
    And I change the page spec to pageGoogle
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I type "lqthang" into element search-field
    And I navigate to url have index 3
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I wait for element mobile-button to be ENABLED
    And I wait for element mobile-button to be EXISTED
    And I click element mobile-button
    And I type "test" into element search-input

  Scenario: test login page
    Given I navigate to url have index 1
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I type "Admin" into element user-field
    And I type "Admin123" into element pass-field
    And I save text for element login-form-title with key "title"
    And I save text for element pass-field with key "Pass"
    And I perform login-page action
    And I change the page spec to IndexPage
#    And I wait for element welcome-user to be DISPLAYED
#    And I wait for element log-out to be DISPLAYED
    And I change the page spec to HomePageOrange
    And I wait for element find-patient-button to be ENABLED
    And I click element find-patient-button
    And I wait for element search-input to be DISPLAYED

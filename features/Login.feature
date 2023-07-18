@testLogin @web @regression
Feature: login web

  @test-1
  Scenario: test login page
    Given I navigate to url have index 1
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I perform login-page-two action with override values
      | Field      | Value     |
      | user-field | Admin     |
      | pass-field | KEY.title |
    And I wait for element error-message to be DISPLAYED
    And I perform login-page-two action with override values
      | Field      | Value    |
      | user-field | Admin    |
      | pass-field | Admin123 |
    And I change the page spec to IndexPage
#    And I wait for element welcome-user to be DISPLAYED
#    And I wait for element log-out to be DISPLAYED
    And I change the page spec to HomePageOrange
    And I wait for element find-patient-button to be ENABLED
    And I click element find-patient-button
    And I wait for element search-input to be DISPLAYED

  @test-2
  Scenario: test page
    Given I navigate to url have index 1
    And I change the page spec to LoginPage
    And I save text for element location-option-inpatient with key "btn-location"
    And I wait for elements with below status
      | Field                     | Value            | Status    |
      | location-option-session   | Inpatient Ward   | DISPLAYED |
      | location-option-session   | Inpatient Ward   | ENABLED   |
      | location-option-session   | KEY.btn-location | DISPLAYED |
      | location-option-inpatient |                  | ENABLED   |
      | location-option-inpatient |                  | EXISTED   |
      | user-field                |                  | DISPLAYED |
      | pass-field                |                  | EXISTED   |
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I save text for element login-form-title with key "title"
    And I type "KEY.title" into element user-field
    And I clear text from element user-field
    And I save text for element location-option-inpatient with key "btn-location"
    And I click element location-option-session with text "KEY.btn-location"
    And I perform login-page-two action with override values
      | Field      | Value     |
      | user-field | Admin     |
      | pass-field | KEY.title |
    And I wait for element error-message to be DISPLAYED
    And I perform input-data action with override values
      | Field      | Value    |
      | user-field | Admin    |
      | pass-field | Admin123 |
    And I wait for element location-option-session with text "Inpatient Ward" to be DISPLAYED
    And I wait for elements with below status
      | location-option-session | Inpatient Ward | DISPLAYED |
    When I click element location-option-session with text "Inpatient Ward"
    Then I click element login-button
#    And I clear text from element field-search
#    And I type "Admidsdsdsn" into element user-field
#    And I type "Admin12dsdsds3" into element pass-field
#    And I click element location-option-inpatient
#    And I wait for element login-button to be ENABLED
#    And I click element login-button
#    And I wait for element error-message to be DISPLAYED
#    And I verify the text for element error-message is "Invalid username/password. Please try again."
#    And I verify the text for element error-message is "Usuario/contraseña inválida. Por favor inténtelo nuevamente."
#    And I navigate to refresh-page
#    And I type "Admin" into element user-field
#    And I type "Admin123" into element pass-field
#    And I save text for element location-option-inpatient with key "location"
#    And I click element location-option-inpatient
#    And I click element login-button


  @login-variant
  Scenario: Variation of Login script. Keeping only overriding values while actions provided in Scenario
    Given I navigate to url have index 1
    When I change the page spec to LoginPage-Variant
    Then I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I save text for element login-form-title with key "title"
    And I type "Admin12dsdsds3" into element pass-field
    Then I perform login-page-three action with override values
      | Field      | Value     |
      | user-field | Admin     |
      | pass-field | KEY.title |
#    Instead of putting actions in Yaml, providing control to the tester
    Then I wait for element location-option-inpatient to be ENABLED
    And I click element location-option-inpatient
    Then I wait for element login-button to be ENABLED
    And I click element login-button
#    ------------------------
    And I wait for element error-message to be DISPLAYED
    And I perform login-page-three action with override values
      | Field      | Value    |
      | user-field | Admin    |
      | pass-field | Admin123 |
#    Instead of putting actions in Yaml, providing control to the tester
    Then I wait for element location-option-inpatient to be ENABLED
    And I click element location-option-inpatient
    Then I wait for element login-button to be ENABLED
    And I click element login-button
#    ------------------------
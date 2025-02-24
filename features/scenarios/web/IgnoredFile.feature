@testLogin @web @regression
Feature: login web for norun

  @test-1
  Scenario: test login page
    Given I navigate to url OPEN_MRS
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
  Scenario: test page test-2
    Given I navigate to url OPEN_MRS
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
  Scenario: Variation of Login script. With some comments
    Given I navigate to url OPEN_MRS
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


#  @login-variant
  Scenario: Another Variation of Login script. Keeping only overriding values while actions provided in Scenario
    Given I navigate to url OPEN_MRS
    When I change the page spec to LoginPage-Variant
    Then I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I save text for element login-form-title with key "title"
    And I type "Admin12dsdsds3" into element pass-field
    Then I perform login-page-three action with override values
      | Field      | Value     |
      | user-field | Admin     |
      | pass-field | KEY.title |

    @verify-element-feature
  Scenario: test feature verify for elements
#    Given I navigate to url OPEN_MRS with options below
#      | options              |
#      | --headless           |
#      | --disable-extensions |
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
      | Field                     | Value           | Status    | Helpers          |
      | user-field                |                 | DISPLAYED |                  |
      | pass-field                |                 | DISPLAYED |                  |
      | location-option-inpatient | Inpatient Ward  | DISPLAYED |                  |
      | location-option-inpatient | In              | DISPLAYED | CONTAINS         |
      | location-option-inpatient | #007FFF         | DISPLAYED | BACKGROUND-COLOR |
      | location-option-inpatient | #FFFFFF         | DISPLAYED | COLOR            |
#      | login-button              | #88af28         | ENABLED   | BACKGROUND-COLOR |Now_ERROR_ON_UBUNTU_AND_MAC_NEED_TO_INVESTIGATE
      | login-button              | #FFFFFF         | ENABLED   | COLOR            |
      | location-option-inpatient | Inpatient       | DISPLAYED | STARTS_WITH      |
      | location-option-inpatient | Inpatient [A-z] | DISPLAYED | REGEX            |
      | location-option-inpatient | Ward            | DISPLAYED | ENDS_WITH        |
#      | location-option-inpatient | OpenSans, Arial, sans-serif | DISPLAYED | FONT_FAMILY      |
#      | location-option-inpatient | 16px                        | DISPLAYED | FONT_SIZE        |
#      | location-option-inpatient | 400                         | DISPLAYED | FONT_WEIGHT      |
#      | location-option-inpatient | 35px                        | DISPLAYED | FONT_HEIGHT      |
#      | location-option-inpatient | left                        | DISPLAYED | TEXT_ALIGN       |
#      | location-option-inpatient | 6                           | DISPLAYED | value            |
#      | location-option-inpatient | 0                           | DISPLAYED | data-key         |
#      | location-option-inpatient | selected                    | DISPLAYED | class            |

  @test-loop-action
  Scenario: test login page
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
     And I loop 10 times for login-and-logout action with polling is 1 seconds with override values
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


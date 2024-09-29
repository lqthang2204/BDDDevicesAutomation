@regression @android

Feature: run regression tech one
  # Enter feature description here

  @T1 @staff-login
  Scenario:  create student from staff
    # Enter steps here
    Given I open application with config below
      | file config                 |
      | capabilities_android_chrome |
    Given I change the page spec to Common
    And I perform by-pass-launch action
  And I navigate to url T1
    And I change the page spec to login_t1_page
    And I perform login-page action
    And I change the page spec to index_t1_page
    And I wait for element menu-ci to be DISPLAYED
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I type "Applications Application" into element search-field
    And I wait for element ApplicationSM-label with text "Applications Admissions and Enrolments - SM" to be DISPLAYED
    And I click element ApplicationSM-label with text "Applications Admissions and Enrolments - SM"

    @T1 @register-student
  Scenario: create student from student portal
    # Enter steps here
  Given I navigate to url T1
    And I change the page spec to login_t1_page
    And I perform login-page action
      And I change the page spec to index_t1_page
    And I wait for element menu-ci with text "Forms" to be DISPLAYED
    And I wait for element search-field to be DISPLAYED
    And I type "Admissions and Enrolments Configuration" into element search-field
    And I wait for element ApplicationSM-label with text "Admissions and Enrolments Configuration" to be DISPLAYED
    And I click element ApplicationSM-label with text "Admissions and Enrolments Configuration"
    And I change the page spec to Admissions_Configuration_page
      And I wait for element section_tab with text "Function Settings" to be DISPLAYED
      And I click element section_tab with text "Function Settings"
      And I wait for element header_text with text "Student Application Registration" to be DISPLAYED
      And I click element header_text with text "Student Application Registration"
      And I wait for element link_register_student to be DISPLAYED
      And I save text for element link_register_student have pattern match "((?<=For example )[\s\S]*)" with key "url_register"
      And I navigate to url KEY.url_register
      And I create a random user
      And I change the page spec to Register_Student_Portal
      And I wait for element spinner to be NOT_DISPLAYED
      And I wait for element family_name_field to be DISPLAYED
       And I create a set of keys with below attributes
         | Pattern to create data from | Save into Key Name |
         | random_alphanumeric_8-12    | family_name        |
         | random_alphanumeric_8       | given              |
      And I wait 1 seconds
      And I create a random user
      And I perform register_applicant action with override values
        | Field            | Value                    |
        | given_name_field | KEY.given                |
        | dob_field        | 10-Oct-2005              |
        | gender_field     | Male                     |
        | email_field      | USER.email               |
        | citizen_field    | Australian Citizen       |
        | password_field   | random_alphanumeric_8-12 |
      And I wait 1 seconds



@regression @web

Feature: run regression tech one
  # Enter feature description here

  @T1 @Application-Data-Entry
  Scenario:  create student from staff
    # Enter steps here
  Given I navigate to url T1
    And I change the page spec to login_t1_page
    And I perform login-page action with override values
    And I change the page spec to index_t1_page
    And I wait for element menu-ci with text "Forms" to be DISPLAYED
    And I wait for element search-field to be DISPLAYED
    And I type "Applications Application" into element search-field
    And I wait for element ApplicationSM-label with text "Applications" to be DISPLAYED
    And I click element ApplicationSM-label with text "Applications"
    And I wait for element ApplicationSM-label to be DISPLAYED
    And I click element ApplicationSM-label
    And I change the page spec to Application_page
    And I wait for element Add-new-Application to be ENABLED
    And I click element Add-new-Application
    And I change the page spec to Create_student_page
    And I wait for element dob to be DISPLAYED
    And I type "10-Oct-2005" into element dob
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element family-name to be DISPLAYED
    And I click element family-name
    And I type "chien" into element family-name
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element given-name to be ENABLED
    And I click element given-name
    And I wait for element spinner to be NOT_DISPLAYED
     And I type "student_{date_current_MMddmm_{random_alphabet_5}" into element given-name
    And I wait for element spinner to be NOT_DISPLAYED
    And I save text for element given-name with key "given_student"
    And I wait for element spinner to be NOT_DISPLAYED
    And I click element email-field
     And I type "chien_nguyen+SAAS-2024B-{KEY.given_student}@technologyonecorp.com" into element email-field
    And I wait for element spinner to be NOT_DISPLAYED
    And I type "student_{date_current_MM-dd-mm}_{random_alphabet_5} " into element middle-name
    And I wait for element Nationality_picker to be ENABLED
    And I click element Nationality_picker
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element Nationality_Au to be DISPLAYED
    And I wait for element spinner to be NOT_DISPLAYED
    And I click element Nationality_Au
    And I wait for element button-page with text "Create new student" to be ENABLED
    And I click element button-page with text "Create new student"
    And I change the page spec to application_data_entry
    #And I wait for element button-page with text "Save" to be ENABLED
    And I wait for element section-menu with text "Student Details" to be ENABLED
    And I click element section-menu with text "Student Details"
    And I change the page spec to student_detail_page
    And I wait for element gender-field to be ENABLED
    And I click element gender-field
    And I clear text from element gender-field
    And I type "Male" into element gender-field
    And I wait for element drop-down-value with text "Male" to be DISPLAYED
    And I wait for element drop-down-value with text "Male" to be ENABLED
    And I click element drop-down-value with text "Male
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element header with text "Addresses" to be DISPLAYED
    And I wait for element address-type-field to be ENABLED
    And I click element address-type-field
    And I type "Mailing" into element address-type-field
    And I wait for element drop-down-value with text "Mailing" to be DISPLAYED
    And I wait for element drop-down-value with text "Mailing" to be ENABLED
    And I click element drop-down-value with text "Mailing
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element element-page with text "Preferred" to be DISPLAYED
    And I wait for element element-page with text "Preferred" to be ENABLED
    And I click element element-page with text "Preferred"
    And I wait for element spinner to be NOT_DISPLAYED
    And I scroll to element header with text "Citizenship and Cultural Details"
    And I wait for element spinner to be NOT_DISPLAYED
#    And I wait for element button-field-country to be ENABLED
#    And I click element button-field-country
#    And I wait for element field-country to be DISPLAYED
#    And I scroll to element field-country
#    And I wait for element field-country to be ENABLED
#    And I perform javascript scrollToElement on element field-country
#    And I perform javascript clickElement on element field-country
#    And I hover-over element field-country
#    And I select the option with the value "Australia" for element field-country
    And I click element field-country
    And I type "Australia" into element field-country
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element drop-down-value with text "Australia" to be DISPLAYED
    And I wait for element drop-down-value with text "Australia" to be ENABLED
    And I click element drop-down-value with text "Australia
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element Addresses_1 to be DISPLAYED
    And I scroll to element Addresses_1
    And I wait for element Addresses_1 to be DISPLAYED
    And I type "123 Ann Street" into element Addresses_1
    And I click element city-field
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element city-field to be DISPLAYED
    And I scroll to element city-field
    And I wait for element city-field to be ENABLED
    And I type "Brisbane" into element city-field
    And I click element state-field
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element state-field to be DISPLAYED
    And I scroll to element state-field
    And I wait for element state-field to be ENABLED
    And I type "NSW" into element state-field
    And I wait for element drop-down-value with text "NSW" to be DISPLAYED
    And I wait for element drop-down-value with text "NSW" to be ENABLED
    And I click element drop-down-value with text "NSW"
    And I wait for element post-code to be DISPLAYED
    And I type "2000" into element post-code
    And I wait for element country-of-birth to be DISPLAYED
    And I type "Australia" into element country-of-birth
     And I wait for element drop-down-value with text "Australia" to be DISPLAYED
    And I wait for element drop-down-value with text "Australia" to be ENABLED
    And I click element drop-down-value with text "Australia"
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element main-language to be ENABLED
    And I type "English" into element main-language
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element save-button to be ENABLED
    And I click element save-button
     And I wait for element spinner to be NOT_DISPLAYED
    And I verify that following elements with below attributes
      | Field        | Value   | Status    | Helpers          |
      | saved-button | Saved   | DISPLAYED | CONTAINS         |
      | saved-button | #74bd00 | DISPLAYED | BACKGROUND-COLOR |

    @T1 @register-student
  Scenario: create student from student portal
    # Enter steps here
  Given I navigate to url T1
    And I change the page spec to login_t1_page
    And I perform login-page action with override values
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
      And I wait 1 seconds
      And I wait for element family_name_field to be DISPLAYED
      And I perform register_applicant action with override values
        | Field             | Value                      |
        | family_name_field | {random_alphanumeric_8-12}            |
        | given_name_field  | {random_alphanumeric_8-12}          |
        | dob_field         | 10-Oct-2005                |
        | gender_field      | Male                       |
        | email_field       | {random_alphanumeric_8-12}              |
        | citizen_field     | Australian Citizen         |
        | password_field    | {random_alphanumeric_8-12}  |
      And I wait 100 seconds



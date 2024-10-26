@regression-tech1 @web

Feature: run regression tech one
  Background: open web T1
    Given I navigate to url T1
  # Enter feature description here

  @T1 @Application-Data-Entry @norun
  Scenario:  create student from staff
    # Enter steps here
    Given I change the page spec to login_t1_page
    And I perform login-page action
    And I change the page spec to index_t1_page
    And I perform javascript getTitle
    And I wait for element menu-ci with text "Forms" to be DISPLAYED
    And I wait for element search-field to be DISPLAYED
    And I type "Applications Application" into element search-field
    And I wait for element ApplicationSM-label with text "Applications" to be DISPLAYED
    And I click element ApplicationSM-label with text "Applications"
    And I change the page spec to Application_page
    And I wait for element Add-new-Application to be ENABLED
    And I click element Add-new-Application
    And I change the page spec to Create_student_page
    And I wait for element dob to be ENABLED
    And I click element dob
     And I wait for element spinner to be NOT_DISPLAYED
    And I type "10-Oct-2005" into element dob
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element family-name to be DISPLAYED
    And I create a random user
    And I click element family-name
    And I type "USER.last_name" into element family-name
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element given-name to be ENABLED
    And I click element given-name
    And I wait for element spinner to be NOT_DISPLAYED
    And I type "USER.first_name" into element given-name
#     And I type "{USER.first_name}{date_current_MMddmm_{random_alphabet_5}" into element given-name
    And I save text for element given-name with key "given_name"
    And I wait for element spinner to be NOT_DISPLAYED
    And I save text for element given-name with key "given_student"
    And I wait for element spinner to be NOT_DISPLAYED
    And I click element email-field
     And I type "chien_nguyen+SAAS-2024B-{KEY.given_student}_{date_current_MMddmm}_{random_alphabet_5}@technologyonecorp.com" into element email-field
    And I wait for element spinner to be NOT_DISPLAYED
#    And I type "student_{date_current_MM-dd-mm}_{random_alphabet_5} " into element middle-name
     And I type "USER.middle_name" into element middle-name
    And I wait for element Nationality_picker to be ENABLED
    And I click element Nationality_picker
    And I wait for element spinner to be NOT_DISPLAYED
    And I perform select_nationality action
#    And I wait for element Nationality_Au to be DISPLAYED
#    And I wait for element spinner to be NOT_DISPLAYED
#    And I click element Nationality_Au
    And I perform close-notification-if-exist action
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
#    And I scroll to element header with text "Citizenship and Cultural Details"
    And I scroll to element header with text "Nationality and Cultural Details"
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
#    And I verify that following elements with below attributes
#      | Field        | Value   | Status    | Helpers          |
#      | saved-button | Saved   | DISPLAYED | CONTAINS         |
#      | saved-button | #74bd00 | DISPLAYED | BACKGROUND-COLOR |
    And I save text for element form-title have pattern match "(\d+)[\s\S]+[a-zA-Z]" with key "student-id"
    And I verify that following elements with below attributes
      | Field              | Value          | Status      | Helpers  |
      | gender-field       | Male           | DISPLAYED   |          |
      | address-type-field | Mailing        | NOT_ENABLED | CONTAINS |
      | field-country      | Australia      | ENABLED     |          |
      | Addresses_1        | 123 Ann Street | ENABLED     |          |
      | city-field         | Brisbane       | ENABLED     |          |
      | state-field        | NSW            | ENABLED     | CONTAINS |
      | post-code          | 2000           | ENABLED     |          |
      | country-of-birth   | Australia      | ENABLED     |          |
      | main-language      | English        | ENABLED     |          |
    And I print all the dictionary keys
    And I change the page spec to application_data_entry
    And I click element section-menu with text "Educational Background"
    And I change the page spec to Educational_Background
    And I wait for element header-background with text "Australian (or Equivalent) Study" to be DISPLAYED
    And I click element Highest-School-Level-Completed
    And I clear text from element Highest-School-Level-Completed
    And I type "Year 8 or below" into element Highest-School-Level-Completed
     And I wait for element drop-down-value with text "Year 8 or below" to be DISPLAYED
    And I click element drop-down-value with text "Year 8 or below"
    And I type "2012" into element year-study
    And I type "random_number_8" into element student-id-field
    And I save text for element student-id-field with key "student_id_random"
    And I click element drop-down-year--school
    And I wait for element External_Organisation_Code to be ENABLED
    And I click element External_Organisation_Code
    And I save text for element year_12_school with key "External_Organisation_Code"
    And I click element state_education
    And I clear text from element state_education
    And I type "Western Australia" into element state_education
    And I save text for element state_education with key "state_education"
    And I wait for element drop-down-value with text "Western Australia" to be ENABLED
    And I click element drop-down-value with text "Western Australia"
    And I wait for element save-button to be ENABLED
    And I click element save-button
    And I change the page spec to application_data_entry
    And I wait for element spinner to be NOT_DISPLAYED
    And I verify that following elements with below attributes
      | Field        | Value   | Status    | Helpers          |
      | saved-button | Saved   | DISPLAYED | CONTAINS         |
      | saved-button | #74bd00 | DISPLAYED | BACKGROUND-COLOR |
     And I wait 1 seconds
     And I change the page spec to Educational_Background
    And I wait for element state_education to be DISPLAYED
    And I verify that following elements with below attributes
      | Field                          | Value                          | Status    | Helpers |
      | Highest-School-Level-Completed | Year 8 or below                | DISPLAYED |         |
      | year-study                     | 2012                           | DISPLAYED |         |
      | student-id-field               | KEY.student_id_random          | DISPLAYED |         |
      | year_12_school                 | KEY.External_Organisation_Code | DISPLAYED |         |
      | state_education                | KEY.state_education            | DISPLAYED |         |
    And I change the page spec to application_data_entry
    And I click element section-menu with text "Courses"
    And I change the page spec to Educational_Background
    And I wait for element show-filter-button to be ENABLED
    And I click element show-filter-button
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element button_add_criteria to be ENABLED
    And I click element button_add_criteria
    And I wait for element select_criteria_field to be DISPLAYED
    And I click element select_criteria_field
    And I type "Year" into element select_criteria_field
    And I wait for element option_criteria_field to be ENABLED
    And I click element option_criteria_field
    And I wait for element value_criteria_field to be ENABLED
    And I click element value_criteria_field
#    And I clear text from element value_criteria_field
    And I execute KEY_DOWN with keyboard CONTROL+a
    And I click keyboard BACKSPACE button on element value_criteria_field
    And I type "2024" into element value_criteria_field
    And I wait for element button_add_index_2 to be ENABLED
    And I click element button_add_index_2
    And I click element select_criteria_field_index_2
    And I type "study Period - Code" into element select_criteria_field_index_2
    And I wait for element option_criteria_field to be ENABLED
    And I click element option_criteria_field
    And I wait for element value_criteria_field_index_2 to be ENABLED
    And I click element value_criteria_field_index_2
    And I clear text from element value_criteria_field_index_2
    And I type "HE Term 3" into element value_criteria_field_index_2
     And I wait for element option_criteria_field_value with text "HE Term 3" to be ENABLED
    And I click element option_criteria_field_value with text "HE Term 3"
    And I click element Natural_Language_Keywords
    And I type "CQ18" into element Natural_Language_Keywords
    And I wait for element button_ok_filter to be ENABLED
    And I click element button_ok_filter
#    And I wait for element spinner to be DISPLAYED
    And I wait for element button_add_course to be ENABLED
    And I click element button_add_course
#    And I wait for element spinner to be DISPLAYED
#    And I wait for element spinner_load_page to be DISPLAYED
#    And I wait 1 seconds
#    And I wait for element search-course to be ENABLED
##    And I wait for element search_button to be ENABLED
#    And I click element search-course
#    And I click keyboard ENTER button on element search-course
#    And I click element search_button
    And I wait for element button_edit_course to be ENABLED
    And I verify that following elements with below attributes
      | Field              | Value | Status  | Helpers |
      | button_edit_course | Edit  | ENABLED |         |
     And I change the page spec to application_data_entry
    And I wait for element more-button to be ENABLED
    And I click element more-button
    And I wait for element more-action with text "Assess" to be ENABLED
    And I click element more-action with text "Assess"
#        And I wait for element spinner_load_page to be DISPLAYED
#    And I wait for element spinner_load_page to be NOT_DISPLAYED
    And I wait for element section-menu with text "Application Contents" to be ENABLED
    And I click element section-menu with text "Application Contents"
    And I change the page spec to Application_Contents
    And I wait for element button-page with text "Assess" to be ENABLED
    And I click element button-page with text "Assess"
    And I wait for element Basis_of_Admission to be DISPLAYED
    And I scroll to element Basis_of_Admission
    And I click element Basis_of_Admission
    And I wait for element cbb_basic_admission to be ENABLED
    And I click element cbb_basic_admission
    And I wait for element option_table_basic_index_1 to be DISPLAYED
    And I click element option_table_basic_index_1
    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element header-page with text "Final Assessment Outcome" to be DISPLAYED
    And I scroll to element header-page with text "Final Assessment Outcome"
    And I wait for element outcome to be DISPLAYED
    And I type "Successful" into element outcome
     And I click element Basis_of_Admission
#    And I wait for element option_picker with text "Successful" to be DISPLAYED
#    And I click element option_picker with text "Successful"
#    And I wait for element spinner to be NOT_DISPLAYED
    And I wait for element button-page with text "Save" to be ENABLED
    And I click element button-page with text "Save"
    And I wait for element button-page with text "View" to be DISPLAYED
    And I wait for element search_toggle to be ENABLED
    And I click element search_toggle
    And I wait for element SearchButton to be ENABLED
    And I loop 10 times for wait-assess-status-for-course action with polling is 5 seconds
    And I wait 2 seconds


  @T1 @register-student @norun
  Scenario: create student from student portal
    # Enter steps here
    Given I change the page spec to login_t1_page
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
            And I create a random user
       And I create a set of keys with below attributes
         | Pattern to create data from | Save into Key Name |
         | random_alphanumeric_8-12    | family_name        |
         | random_alphanumeric_8       | given              |
         | random_alphanumeric_12      | password           |
       And I perform operations with below attributes
         | Left                                                       | Operator | Right                  | SaveAs       |
         | chien_nguyen+SAAS-2024B-{USER.first_name}_{USER.last_name} | concat   | @technologyonecorp.com | unique-gmail |
      And I perform register_applicant action with override values
        | Field            | Value              |
        | given_name_field | USER.last_name     |
        | dob_field        | 10-Oct-2005        |
        | gender_field     | Male               |
        | email_field      | KEY.unique-gmail   |
        | citizen_field    | Australian Citizen |
      And I wait for element term_and_condition to be ENABLED
      And I click element term_and_condition
      And I wait for element spinner to be NOT_DISPLAYED
      And I click element term_and_condition
      And I wait for element register-button to be ENABLED
      And I click element register-button
      And I wait for element continue-button to be ENABLED
      And I click element continue-button
      And I change the page spec to make_application
      And I wait for element search-course to be DISPLAYED
      And I type "Associate Degree of Computer Systems" into element search-course
      And I click element search-button
      And I wait for element spinner to be NOT_DISPLAYED
      And I wait for element course-section to be DISPLAYED
      And I wait for element add-to-application-button to be ENABLED
      And I click element add-to-application-button
      And I wait for element spinner to be NOT_DISPLAYED
      And I wait for element message to be DISPLAYED
      And I wait for element next-button to be ENABLED
      And I click element next-button
      And I wait for element header-section with text "Select a Scholarship" to be DISPLAYED
      And I wait for element next-button to be ENABLED
      And I click element next-button
      And I wait for element header-section with text "Apply For Advanced Standing" to be DISPLAYED
      And I wait for element next-button to be ENABLED
      And I click element next-button
       And I wait for element header-section with text "Applicant Details" to be DISPLAYED
      And I perform input_application_detail action with override values
        | Field                | Value                        |
        | phone-number         | random_number_8              |
        | Country              | Australia                    |
        | address              | Male                         |
        | city                 | Brisbane                     |
        | state                | Australian Capital Territory |
        | postcode             | 2000                         |
        | country_of_birth     | Australia                    |
        | main_language        | English                      |
        | Proficiency_language | Very good                    |
      And I wait for element next-button to be ENABLED
      And I click element next-button
      And I wait 5 seconds




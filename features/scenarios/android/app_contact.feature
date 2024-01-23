@test-app-contact @mobile @android
Feature:  mobile with contact

  @test-app-contact
  Scenario: test app contact android
        Given I open application with config below
          | file config                      |
          | capabilities_app_contact_android |
    Given I change the page spec to index_contact
    And I wait for element contact-button to be ENABLED
    And I wait for element create-contact-button to be ENABLED
    And I click element create-contact-button
    And I create a random user
    And I change the page spec to create_contact_page
#    And I type "KEY.title" into element user-field
    And I type "USER.first_name" into element first-name
    And I type "USER.last_name" into element last-name
    And I wait for element save-contact-button to be ENABLED
    And I click element save-contact-button
    And I change the page spec to profile_user
#    And I wait for element full-name to be DISPLAYED
    And I verify that following elements with below attributes
      | Field     | Value          | Status    | Helpers |
      | full-name | USER.full_name | DISPLAYED | text    |

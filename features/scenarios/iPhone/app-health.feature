@test-app-clock @mobile @ios
Feature:  mobile ios

  @test-app-health
  Scenario: test app health ios
    Given I open application with config below
      | file config |
      | capabilities_app_health_ios            |
     And I close application
    And I open application with config below
      | file config |
      | capabilities_app_health_ios            |
#    And I close application
    Given I change the page spec to index_health
    And I click element continue-button
    And I wait for element continue-button-page-2 to be ENABLED
    And I click element continue-button-page-2
    And I change the page spec to detail_health_page
    And I verify that following elements with below attributes
      | Field            | Value    | Status    | Helpers     |
      | first-name       |          | ENABLED   |             |
      | last-name        |          | ENABLED   |             |
      | dob              |          | ENABLED   |             |
      | sex              |          | ENABLED   |             |
      | height           |          | ENABLED   |             |
      | weight           |          | DISPLAYED |             |
      | first-name-field | Optional | DISPLAYED |             |
      | first-name-field | O[a-z]   | DISPLAYED | REGEX       |
      | first-name-field | al       | DISPLAYED | CONTAINS    |
      | first-name-field | O        | DISPLAYED | STARTS_WITH |
      | first-name-field | al       | DISPLAYED | ENDS_WITH   |
    And I create a random user
    And I click element first-name
    And I clear text from element first-name
    And I type "USER.first_name" into element first-name
    And I clear text from element last-name
    And I type "USER.last_name" into element last-name
    And I wait for element done-button to be ENABLED
    And I click element done-button
    And I click element dob
#    And I drag and drop element date-picker-month to element first-name
   And I type "March" into element date-picker-month

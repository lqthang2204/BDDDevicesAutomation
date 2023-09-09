@test-app-clock @mobile @ios
Feature:  mobile ios

  @test-app-health
  Scenario: test app health ios
    Given I change the page spec to index_health
    And I click element continue-button
    And I wait for element continue-button-page-2 to be ENABLED
    And I click element continue-button-page-2
    And I change the page spec to detail_health_page
    And I wait for element with text
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
    When I type "USER.first_name" into element first-name
    Then I type "USER.last_name" into element last-name
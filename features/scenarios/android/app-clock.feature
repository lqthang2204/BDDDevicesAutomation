@test-app-clock @mobile @android
Feature:  mobile

  @test-app-clock1
  Scenario: test app clock android
    Given I open application with config below
      | file config          |
      | capabilities_android |
    Given I change the page spec to clock_page
    And I verify that following elements with below attributes
      | Field        | Value | Status  | Helpers |
      | clock-button |       | ENABLED |         |
      | alarm-button |       | ENABLED |         |
    And I click element alarm-button
    And I change the page spec to alarm_page
    And I wait for element add-alarm-button to be ENABLED
    And I click element add-alarm-button
    And I wait for element cancel-button to be ENABLED
    And I verify that following elements with below attributes
      | Field         | Value  | Status    | Helpers     |
      | cancel-button | CANCEL | ENABLED   |             |
      | cancel-button | C[A-Z] | ENABLED   | REGEX       |
      | cancel-button | EL     | ENABLED   | CONTAINS    |
      | cancel-button | C      | ENABLED   | STARTS_WITH |
      | cancel-button | EL     | ENABLED   | ENDS_WITH   |
      | cancel-button | CANCEL | DISPLAYED | text        |
@app-health @mobile @ios
Feature:  mobile ios

  @test-app-health @app-health
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
    And I click element browse-button
    And I change the page spec to browse_page
    And I verify that following elements with below attributes
      | Field             | Value             | Status  | Helpers  |
      | activity          | Activity          | ENABLED |          |
      | Body_Measurements | Body Measurements | ENABLED |          |
      | Cycle_Tracking    | Cycle             | ENABLED | CONTAINS |
      | Hearing           | H[a-z]            | ENABLED | REGEX    |
    And I perform verify-fields action

      @test-app-health-2 @app-health
  Scenario: test app health ios 2
    Given I open application with config below
      | file config |
      | capabilities_app_health_ios            |
     And I close application
    And I open application with config below
      | file config |
      | capabilities_app_health_ios            |
#    And I close application
    Given I change the page spec to index_health
    And I click element browse-button
    And I change the page spec to browse_page
    And I verify that following elements with below attributes
      | Field             | Value             | Status  | Helpers  |
      | activity          | Activity          | ENABLED |          |
      | Body_Measurements | Body Measurements | ENABLED |          |
      | Cycle_Tracking    | Cycle             | ENABLED | CONTAINS |
      | Hearing           | H[a-z]            | ENABLED | REGEX    |
    And I perform verify-fields action





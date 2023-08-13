@api
Feature: API POST demo two


  @api
  Scenario: DEMO for POST call in API two
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue              |
      | Authorization | Bearer 00D8E000000Hq7R!
      | Content-Type  | application/json        |
    And I set payload json_demo_payload2 with below attributes
    And I trigger POST call with below attributes
    Then I verify response code with status is "400"


@api
Feature: API GET demo two


  @api
  Scenario: DEMO two for GET call in API - Failing sceanrio
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue                                                                                                  |
      | Authorization | Bearer 00D8E000000Hq7R!.E2rCtRRXwyCApuDtUAIx_6A |
      | Content-Type  | application/json                                                                                            |
    And I set payload json_demo_payload with below attributes
    And I trigger POST call with below attributes
      | FieldName | fieldValue |
    Then I verify the response with below attributes
      | FieldName | fieldValue |


@api
Feature: API POST demo one


  @api @harshpost
  Scenario: DEMO for POST call in API one
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue                 |
      | Authorization | Bearer 00D8E000000Hq7R!AQ4 |
      | Content-Type  | application/json           |
    And I set payload json_demo_payload with below attributes
    And I trigger POST call with below attributes
    Then I verify response code with status is "200"
    Then I verify response body with below attributes
      | FieldName               | FieldValue | Helpers  |
      | $.graph[0].isSuccessful | true       | EQUAL    |
      | $.graph[0].isSuccessful | true       | NOT_NULL |
      | $.graph[0].body.id      |            | NOT_NULL |
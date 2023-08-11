@api
Feature: API GET demo one


  @api @tanuj
  Scenario: DEMO for GET call in API one
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue                                                                                                              |
      | Authorization | Bearer 00D8E000000Hq7R!AQ4AQEwLwc995l4rGImqo5Cv0cofIVnDWgteWKo2E_WWj5IykiLg4wIfyaS53VRR4JF9s0BIKgJgnq9U1ie5WIKidJzy_2nl |
      | Content-Type  | application/json                                                                                                        |
    And I set payload json_demo_payload with below attributes
    And I trigger POST call with below attributes
    Then I verify response code with status is "200"
    Then I verify response body with below attributes
      | FieldName | FieldValue | Helpers  |
      | id        |            | NOT_NULL |
#      | PersonEmail | AutoGenEmail_yUregTnJbXt9FPeX8pgr@Test.com | EQUAL    |
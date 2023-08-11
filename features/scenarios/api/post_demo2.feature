@api
Feature: API GET demo two


  @api
  Scenario: DEMO for GET call in API two
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue                                                                                                              |
      | Authorization | Bearer 00D8E000000Hq7R!AQ4AQFfP5wbkowYdFf1EWunD9wxr92czkSYIEP70jRRKMPCOGkYaC5nFHWyQx23MU3ULZgyrwm83fI4I2sZjWn4metlkX2WU |
      | Content-Type  | application/json                                                                                                        |
    And I set payload json_demo_payload2 with below attributes
    And I trigger POST call with below attributes
      | FieldName | fieldValue |
      | dfas dfas | asdfasd fa |
    Then I verify response code with status is "400"


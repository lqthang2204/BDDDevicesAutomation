@api
Feature: API GET demo one


  @api @harshget @get
  Scenario: DEMO for GET call in API one
    Given I set apifacet as SFCLOUD for endpoint Get-Location
    And I set headers with below attributes
      | FieldName     | fieldValue                   |
      | Authorization | Bearer eyJ0eXAiOiJKV1QiLCJhb |
      | Content-Type  | application/json             |
    And I trigger GET call with below attributes
      | Operation Level | AttributeName | AttributeValue |
      | Path            | orgId         | THE_ORG        |
      | Path            | locationType  | CENTRE         |
      | Path            | locationId    | 12345          |
    Then I verify response code with status is "200"
    Then I verify response body with below attributes
      | FieldName                   | FieldValue | Helpers  |
      | $.workingCalendar.startTime | 00:00      | EQUAL    |
      | $.workingCalendar.startTime |            | NOT_NULL |
      | $.workingCalendar.endTime   | 06:00      | EQUAL    |
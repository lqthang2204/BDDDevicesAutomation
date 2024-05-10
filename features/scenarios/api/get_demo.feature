@api @fast @norun
Feature: API GET demo one


  @api @harshget @get
  Scenario: DEMO for GET call in API one
    Given I set apifacet as SFCLOUD-TOKEN without endpoint
    And I set form sfcloud_token with below attributes
    Then I trigger POST call with below attributes
    Then I verify response body with below attributes
      | FieldName      | FieldValue | Helpers          |
      | $.access_token |            | KEY.access_token |
    Given I set apifacet as SFCLOUD for endpoint Get-Location
    And I set headers with below attributes
      | FieldName     | fieldValue       |
      | Authorization | KEY.access_token |
      | Content-Type  | application/json |
    And I trigger GET call with below attributes
      | Operation Level | AttributeName | AttributeValue |
      | Path            | orgId         | ORGNAME        |
      | Path            | locationType  | LOCNAME        |
      | Path            | locationId    | 12345          |
    Then I verify response code with status is "200"
    Then I verify response body with below attributes
      | FieldName                   | FieldValue | Helpers  |
      | $.workingCalendar.startTime | 00:00:00   | EQUAL    |
      | $.workingCalendar.startTime |            | NOT_NULL |
      | $.workingCalendar..endTime  | 23:59:59   | EQUAL    |
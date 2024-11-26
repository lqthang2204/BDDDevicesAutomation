@api @fast @norun
Feature: API POST demo one


  @harshpost1
  Scenario: DEMO for POST call in API one
    Given I set apifacet as SFCC-TOKEN without endpoint
    And I set form sfcc-token with below attributes
    Then I trigger POST call request with below attributes
    Then I verify response body with below attributes
      | FieldName      | FieldValue | Helpers          |
      | $.access_token |            | KEY.access_token |
    Given I set apifacet as SFCC for endpoint Composite-Graph
    And I set headers with below attributes
      | FieldName     | fieldValue       |
      | Authorization | KEY.access_token |
      | Content-Type  | application/json |
    Given I create a set of keys with below attributes
      | Pattern to create data from | Save into Key Name  |
      | random_alphabet_15          | randomAplhabetLen15 |
      | random_number_10            | randomNumLen10      |
      | uuid                        | ExternalId          |
    Given I perform operations with below attributes
      | Left                | Operator | Right              | SaveAs       |
      | randomAplhabetLen15 | concat   | @somedomainabc.com | unique-gmail |
    And I set payload json_demo_payload with below attributes
      | FieldName       | fieldValue         |
      | body.Email      | KEY.unique-gmail   |
      | body.LoginEmail | KEY.unique-gmail   |
      | SecLoginEmail   | KEY.randomNumLen10 |
      | body.ExternalId | KEY.ExternalId     |
    And I trigger POST call request with below attributes
    Then I verify response code with status is "200"
    Then I verify response body with below attributes
      | FieldName                | FieldValue | Helpers  |
      | $.graphs[0].isSuccessful |            | NOT_NULL |
      | $.graphs[0].body.id      |            | NOT_NULL |
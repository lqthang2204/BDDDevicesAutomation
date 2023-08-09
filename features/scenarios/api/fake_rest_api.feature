@api_fake_rest
Feature: test api with fake rest api


  @fake_rest_api_1
  Scenario: DEMO scenario1
    Given I set apifacet as FAKERESTAPI for endpoint Activity
    And I set headers with below attributes
      | FieldName    | fieldValue        |
      | Content-Type | text/plain; v=1.0 |
    And I trigger GET call with below attributes
    And I verify response code with status is "200"
    And I verify response header with below attributes
      | FieldName              | FieldValue | Helpers  |
      | Server                 | Kestrel    | NOT_NULL |
      | Server                 | Kestrel    | ALPHABET |
      | api-supported-versions | 1.0        | NUMERIC  |
      | Date                   |            | NOT_NULL |
      | test                   |            | NULL     |
    Then I verify response body with below attributes
      | FieldName | FieldValue | Helpers  |
      | dueDate   |            | NOT_NULL |
      | title     |            | NOT_NULL |
      | completed | False      | ALPHABET |
      | id        |            | NUMERIC  |


    @fake_rest_api_2
    Scenario: DEMO API without endpoint
    Given I set apifacet FAKERESTAPI without endpoint
    And I set headers with below attributes
      | FieldName    | fieldValue        |
      | Content-Type | text/plain; v=1.0 |
    And I trigger GET call with below attributes
    Then I verify response code with status is "200"
    Then I verify response header with below attributes
      | FieldName              | FieldValue | Helpers  |
      | Server                 | Kestrel    | NOT_NULL |
      | Server                 | Kestrel    | ALPHABET |
      | api-supported-versions |            | NULL     |
      | Date                   |            | NOT_NULL |
      | test                   |            | NULL     |
      | Transfer-Encoding      | chunked    |          |
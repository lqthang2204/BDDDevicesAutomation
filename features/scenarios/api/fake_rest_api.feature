@api @api_fake_rest @get @fast
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
      | api-supported-versions | 1.0        |          |
      | Date                   |            | NOT_NULL |
    And I verify response body with below attributes
      | FieldName     | FieldValue     | Helpers  |
      | [0].id        | 1              | NUMERIC  |
      | [0].title     | Activity 1     |          |
      | [*].title     | Activity [0-9] | REGEX    |
      | [*].title     | [A-z] [0-9]    | REGEX    |
      | [*].dueDate   |                | NOT_NULL |
      | [0].completed | False          | BOOL     |


  @fake_rest_api_2
    Scenario: DEMO API without endpoint
    Given I set apifacet as FAKERESTAPI without endpoint
    And I set headers with below attributes
      | FieldName    | fieldValue        |
      | Content-Type | text/plain; v=1.0 |
    And I trigger GET call with below attributes
    And I verify response code with status is "200"
    Then I verify response header with below attributes
      | FieldName         | FieldValue | Helpers  |
      | Server            | Kestrel    | NOT_NULL |
      | Server            | Kestrel    | ALPHABET |
      | Date              |            | NOT_NULL |
      | Transfer-Encoding | chunked    |          |

     @fake_rest_api_3
    Scenario: DEMO api use key-value to verify response data
    Given I navigate to url OPEN_MRS
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I type "johan" into element user-field
    And I save text for element user-field with key "user-name"
    And I set apifacet as FAKERESTAPI for endpoint Create_Activity
    And I set headers with below attributes
      | FieldName    | fieldValue                             |
      | Content-Type | application/json; charset=utf-8; v=1.0 |
    And I set payload fake_rest_api with below attributes
      | FieldName | fieldValue    |
      | title     | KEY.user-name |
    And I trigger POST call with below attributes
    And I verify response body with below attributes
      | FieldName | FieldValue | Helpers |
      | $.id      | 1          | NUMERIC |
      | $.title   | johan      |         |
    And I verify response body with below attributes
      | FieldName | FieldValue    | Helpers |
      | $.id      | 1             | NUMERIC |
      | $.title   | KEY.user-name |         |

 @fake_rest_api_4
  Scenario: DEMO polling GET Method
    Given I set apifacet as FAKERESTAPI for endpoint Activity
    And I set headers with below attributes
      | FieldName    | fieldValue        |
      | Content-Type | text/plain; v=1.0 |
    And I trigger GET call with below attributes
    And I verify response code with status is "200"
   And I poll the GET call "10" times until below conditions
     | FieldName     | FieldValue | Helpers |
     | response_code | 200        |         |
     | [0].id        | 1          | NUMERIC |


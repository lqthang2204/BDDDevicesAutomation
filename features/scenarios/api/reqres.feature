@api @api_reqres
Feature: test api with fake rest api


  @reqres_api_1
  Scenario: DEMO reqres scenario 1
    Given I set apifacet as REQRES for endpoint Get-Users
    And I trigger GET call request
    And I verify response code with status is "200"
    And I verify response header with below attributes
      | FieldName       | FieldValue      | Helpers |
      | Age             |                 | NUMERIC |
      | Report-To       | 3600            | CONTAIN |
      | Vary            | Accept-Encoding | EQUAL   |
      | CF-Cache-Status | HIT             |         |
    And I verify response body with below attributes
      | FieldName    | FieldValue          | Helpers |
      | page         | 2                   | NUMERIC |
      | data[0].id   |                     | NUMERIC |
      | support.text | Tired of writing endless social media content? Let Content Caddy generate it for you. | CONTAIN |

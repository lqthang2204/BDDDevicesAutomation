@test_api @web
Feature: orange HRM web

  @get_user
  Scenario: perform accessibility testing on TECHPANDA
    Given I navigate to url GOOGLE
    And I change the page spec to pageGoogle
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I set apifacet as REQRES for endpoint Get-Users
    And I trigger GET call request
    And I verify response code with status is "200"
    And I verify response header with below attributes
      | FieldName       | FieldValue      | Helpers |
      | Age             |                 | NUMERIC |
      | Report-To       | 3600            | CONTAIN |
      | Vary            | Accept-Encoding | EQUAL   |
      | CF-Cache-Status | HIT             |         |
    And I verify response body with below attributes
      | FieldName    | FieldValue                                                                            | Helpers |
      | page         | 2                                                                                     | NUMERIC |
      | data[0].id   |                                                                                       | NUMERIC |
      | support.text | Tired of writing endless social media content? Let Content Caddy generate it for you. | CONTAIN |
#    And I save text for response with below attributes
#      | FieldName    | unique      |
#      | page         | page        |
#      | data[0].id   | user_id     |
#      | support.text | support_key |
    And I print all the dictionary keys
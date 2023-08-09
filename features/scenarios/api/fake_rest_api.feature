@api_fake_rest
Feature: test api with fake rest api


  @fake_rest_api_1
  Scenario: DEMO scenario1
    Given I set apifacet as FAKERESTAPI for endpoint Activity
    And I set headers with below attributes
      | FieldName    | fieldValue        |
      | Content-Type | text/plain; v=1.0 |
    And I trigger GET call with below attributes
#    This needs to be updated as the Issue #30
    Then I verify the response with below attributes
      | FieldName       | FieldValue             |
      | Response Code   | 200                    |
      | Response Header | Server Equal Kestrel   |
      | Response Body   | title Equal Activity 2 |


  @fake_rest_api_2
  Scenario: DEMO scenario2
    Given I set apifacet as GOREST for endpoint Get-Users
    And I set headers with below attributes
      | FieldName | fieldValue       |
      | Accept    | application/json |
      #    This needs to be updated as the Issue #30
    And I trigger GET call with below attributes
      | FieldName | fieldValue  |
      | params    | page=1      |
      | params    | per_page=20 |
      #    This needs to be updated as the Issue #30
    Then I verify the response with below attributes
      | FieldName       | FieldValue                                                        |
      | Response Code   | 200                                                               |
      | Response Header | x-links-current Equal https://gorest.co.in/public/v2/users?page=1 |
      | Response Body   | email Equal ahluwalia_vasudev@leannon.example                                            |
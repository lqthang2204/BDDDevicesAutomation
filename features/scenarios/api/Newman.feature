# Created by admin at 12/11/2024
Feature: Demo features run newman
  # Enter feature description here

  @newman @api
  Scenario: run newman without data, method get
    Given I navigate to url GURU99
    And I run postman collection file apichallenges.postman_collection.json
    # Enter steps here

    @newman @api @apichallenges3
  Scenario: run newman with multi collection
    Given I navigate to url GURU99
    And I run postman collection file apichallenges3.postman_collection.json

          @newman @api @apichallenges4
  Scenario: run newman with collection and data file
    Given I navigate to url GURU99
    And I run postman collection file apichallenges4.postman_collection.json with data file apichallenges_2.data.json


          @newman @api @apichallenges5
  Scenario: run newman with collection and data file
#    Given I navigate to url GURU99
    And I create a random user
    And I run postman collection file apichallenges4.postman_collection.json with data file apichallenges_2.json with override value
      | Field | Value            |
      | name  | USER.first_name |


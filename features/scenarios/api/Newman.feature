# Created by admin at 12/11/2024
Feature: Demo features run newman
  # Enter feature description here

  @newman @api
  Scenario: run newman without data, method get
    Given I navigate to url GURU99
    And I run postman collection with file apichallenges.postman_collection.json
    # Enter steps here
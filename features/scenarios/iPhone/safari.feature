@test-app-clock @mobile @ios
Feature:  mobile ios

  @safari_drag_and_drop
  Scenario: run safari to test drag and drop feature
    Given I change the page spec to mobile-drag-drop
    And I navigate to url CODESANDBOX
    And I wait for element click-run-button to be ENABLED
    And I click element click-run-button
    And I wait for element 1a-button to be DISPLAYED
    And I hover-over element 1a-button
   And I drag and drop element 1a-button to element 2a-button
#    And I click element continue-button
#    And I wait for element continue-button-pageÏ-2 to be ENABLED
#    And I click element continue-button-page-2
#    And I change the page spec to detail_health_page
#    And I verify that following elements with below attributes
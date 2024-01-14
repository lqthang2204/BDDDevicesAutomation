@test-app-clock @mobile @android
Feature:  mobile android

  @chrome_drag_and_drop
  Scenario: run chrome to test drag and drop feature
        Given I open application with config below
          | file config |
          | capabilities_android_chrome            |
    Given I change the page spec to Common
    And I perform by-pass-launch action
    And I change the page spec to mobile-drag-drop
    And I navigate to url CODESANDBOX
    And I wait for element click-run-button to be ENABLED
    And I click element click-run-button
    And I wait for element 1a-button to be DISPLAYED
    And I hover-over element 1a-button
   And I drag and drop element 1a-button to element 2a-button
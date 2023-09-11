@web @regression @drag-drop
Feature: test feature drag and drop

  @drag-drop-1
  Scenario: test drag and drop 1
    Given I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
    And I hover-over element bank_label
    And I drag and drop element bank_label to element debit_side
    And I wait 5 seconds

  @drag-drop-2
  Scenario: test drag and drop 2
    Given I navigate to url GLOBAL_SQA
    And I change the page spec to drag_global
    And I wait for element image with text "High Tatras" to be DISPLAYED
#    And I wait for element debit_side to be DISPLAYED
#    And I hover-over element bank_label
#    And I drag and drop element bank_label to element debit_side
#    And I wait 5 seconds


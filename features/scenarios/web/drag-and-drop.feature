@web @regression @drag-drop
Feature: test feature drag and drop

  @drag-drop-1
  Scenario: test login page
    Given I navigate to url GURU99
    And I change the page spec to demoguru99
    And I wait for element bank_label to be DISPLAYED
    And I wait for element debit_side to be DISPLAYED
    And I save coordinates for element debit_side with key "debit_dimension"
    And I hover-over element bank_label
    And I drag and drop element bank_label to element debit_side
#    And I drag and drop element bank_label to coordinates KEY.debit_dimension
    And I wait 100 seconds

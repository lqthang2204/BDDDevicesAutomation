@test-tiki-total
    Feature: navigate URL

      @test-tiki-1
      Scenario: test login page
        Given I navigate to url have index 4
        And I change the page spec to indexTiki
        And I wait for element icon-cart to be DISPLAYED
        And I wait for element seach-input to be DISPLAYED
        And I click element seach-input
        And I wait for element field-search to be DISPLAYED
        And I type "quat tich dien" into element field-search
        And I wait for element result-search to be DISPLAYED
  #    And I clear text from element seach-input
  #    And I wait for element pass-field to be DISPLAYED
  #    And I type "Admin" into element user-field
  #    And I type "Admin123" into element pass-field
  #    And I click element login-button

    @test-tiki-2
      Scenario: test login page
      Given I navigate to url have index 4
      And I change the page spec to indexTiki
      And I wait for element icon-cart to be DISPLAYED
      And I wait for element menu-danh-muc to be ENABLED
      And I click element menu-danh-muc
#      And I wait for element seach-input to be DISPLAYED
#      And I click element seach-input
#      And I wait for element field-search to be DISPLAYED
#      And I type "quat tich dien" into element field-search
#      And I wait for element result-search to be DISPLAYED
  #    And I clear text from element seach-input
  #    And I wait for element pass-field to be DISPLAYED
  #    And I type "Admin" into element user-field
  #    And I type "Admin123" into element pass-field
  #    And I click element login-button


Feature: navigate URL
#  @Windows10_Chrome_76.0
#  @Windows10_Firefox_68.0
  Scenario: negative to url
    Given I navigate to "https://www.google.com/"
    And I change the page spec to pageGoogle
    And I click element search-field
    And I type "lqthang" into element search-field
    And I navigate to "https://demo.guru99.com/test/guru99home/"
    And I change the page spec to index_guru
    And I click element selenium icon
    And I navigate to "https://www.google.com/"
    And I change the page spec to pageGoogle
    And I type "dsds" into element search-field

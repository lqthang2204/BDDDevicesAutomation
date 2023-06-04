Feature: navigate URL
  Scenario: negative to url
    Given I navigate to "https://www.google.com/"
    And I change the page spec to pageGoogle
    And I click element search-field
     And I type "lqthang" into element search-field
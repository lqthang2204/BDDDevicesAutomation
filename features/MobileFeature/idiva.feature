@test-idiva-total
    Feature: navigate URL

      @test-idiva-1
      Scenario: test login page
        Given I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be DISPLAYED
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I wait for element fashion-female to be DISPLAYED
        And I wait for element fashion-male to be DISPLAYED
        And I wait for element sneaker-product to be DISPLAYED
        And I wait for element sneaker-product to be DISPLAYED
        And I wait for element bag-product to be DISPLAYED
        And I save text for element fashion-female with key "pr-bag"
        And I click element sneaker-product
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED

      @test-idiva-2
      Scenario: test login page
        Given I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be DISPLAYED
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I wait for element sneaker-product to be DISPLAYED
        And I perform verify-menu action
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED
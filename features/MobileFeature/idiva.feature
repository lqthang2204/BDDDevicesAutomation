@test-idiva-total @mobile
    Feature: idiva mobile
      @test-idiva-1
      Scenario: idiva-1
        Given I change the page spec to Common
        And I perform by-pass-launch action
        And I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I perform click-menu-if-exist action
        And I wait for element fashion-female to be DISPLAYED
        And I wait for element fashion-male to be DISPLAYED
        And I wait for element sneaker-product to be DISPLAYED
        And I wait for element sneaker-product to be DISPLAYED
        And I wait for element bag-product to be DISPLAYED
        And I save text for element fashion-female with key "pr-bag"
        And I click element sneaker-product
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED

      @test-idiva-2 @MUTE
      Scenario: idiva-2 mobile
        Given I change the page spec to Common
        And I perform by-pass-launch action
        And I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be DISPLAYED
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I wait for element sneaker-product to be DISPLAYED
        And I perform verify-menu action
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED

      @test-idiva-3
      Scenario: search productmobile
        Given I change the page spec to Common
        And I perform by-pass-launch action
        And I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be DISPLAYED
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I wait for element sneaker-product to be DISPLAYED
        And I perform verify-menu action
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED
        And I save text for element item-sneaker with key "sneaker"
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I perform search-sneaker action with override values
          | Field          | Value       |
          | search-product | KEY.sneaker |
#        And I wait for element search-product to be DISPLAYED
#        And I type "KEY.sneaker" into element search-product
#        And I wait for element btn-search to be ENABLED
#        And I click element btn-search

        @test-idiva-3
      Scenario: search productmobile
        Given I change the page spec to Common
        And I perform by-pass-launch action
        And I navigate to url have index 5
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be DISPLAYED
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I wait for element sneaker-product to be DISPLAYED
        And I perform verify-menu action
        And I change the page spec to product_sneaker
        And I wait for element sort-product to be DISPLAYED
        And I save text for element item-sneaker with key "sneaker"
        And I change the page spec to Home_idiva
        And I wait for element menu-toogle to be ENABLED
        And I click element menu-toogle
        And I perform search-sneaker action with override values
          | Field          | Value       |
          | search-product | KEY.sneaker |

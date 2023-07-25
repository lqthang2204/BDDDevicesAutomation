@test-tiki-total @mobile
    Feature: tiki mobile


      @test-tiki-3
      Scenario: test tiki 3
#      Given I open application
      Given I change the page spec to HomeTiki
#      And I wait for element icon-at-page-home with text "Trang chủ" to be DISPLAYED
#      And I wait for element icon-at-page-home with text "Danh mục" to be DISPLAYED
#      And I wait for element icon-at-page-home with text "Tin mới" to be DISPLAYED
#      And I wait for element icon-at-page-home with text "navigation_navigate_profile" to be DISPLAYED
#      And I wait for element icon-at-page-home with text "Astra" to be DISPLAYED
      And I wait for elements with below status
        | Field             | Value     | Status    |
        | icon-at-page-home | Trang chủ | DISPLAYED |
        | icon-at-page-home | Trang chủ | DISPLAYED |
        | icon-at-page-home | Trang chủ | DISPLAYED |
        | icon-at-page-home | Trang chủ | DISPLAYED |
        | icon-at-page-home | Trang chủ | DISPLAYED |


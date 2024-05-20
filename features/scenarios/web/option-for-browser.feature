@test-options @web
Feature: add option for browser


#  Some of the more commonly used Chrome startup arguments include:
#
#Argument	                      Usage
#--start-maximized	                  Opens Chrome in maximize mode
#incognito	                      Opens Chrome in incognito mode
#headless	                      Opens Chrome in headless mode
#disable-extensions	              Disables existing extensions on Chrome browser
#--disable-popup-blocking	          Disables pop-ups displayed on Chrome browser
#make-default-browser	          Makes Chrome default browser
#version	                          Prints chrome browser version
#disable-infobars	              Prevents Chrome from displaying the notification ‘Chrome is being controlled by automated software
#  list option for chrome : https://gist.github.com/ntamvl/4f93bbb7c9b4829c601104a2d2f91fe5
  @option-for-arguments
  Scenario: test options arguments browser
    Given I navigate to url OPEN_MRS with options below
      | options  | value                    |
      | argument | --disable-infobars       |
      | argument | --disable-extensions     |
      | argument | --no-sandbox             |
      | argument | --headless           |
      | argument | --disable-popup-blocking |
      | argument | --incognito              |
      | argument | --lang=fr                |
#      | argument | --proxy-server=192.168.0.1:8080 |
#      | argument | --window-size=600,719           |
    And I change the page spec to LoginPage
    And I wait for element user-field to be DISPLAYED
    And I wait for element pass-field to be DISPLAYED
    And I save text for element login-form-title with key "title"
    And I perform login-page-two action with override values
      | Field      | Value     |
      | user-field | Admin     |
      | pass-field | KEY.title |
    And I wait 10 seconds
    And I wait for element error-message to be DISPLAYED
    And I perform login-page-two action with override values
      | Field      | Value    |
      | user-field | Admin    |
      | pass-field | Admin123 |

      @option-popup @safari
  Scenario: option popup prevent
    Given I navigate to url GURU99-DOUBLE with options below
      | options  | value |
      | argument |    --disable-popup-blocking   |
        And I change the page spec to double-example
    And I wait for element double-button to be ENABLED
    And I double-click element double-button
    And I accept for popup
    And I double-click element double-button
    And I dismiss for popup
    And I right-click element right-button
    And I wait for element edit-button to be DISPLAYED
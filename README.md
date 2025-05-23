[![Releases downloads](https://img.shields.io/github/downloads/lqthang2204/BDDDevicesAutomation/total.svg)](https://github.com/lqthang2204/BDDDevicesAutomation/releases)
[![Build Status](https://github.com/lqthang2204/BDDDevicesAutomation/actions/workflows/project-runner-windows.yml/badge.svg)](https://github.com/lqthang2204/BDDDevicesAutomation/actions)
[![GitHub last commit](https://img.shields.io/github/last-commit/lqthang2204/BDDDevicesAutomation.svg)](https://github.com/lqthang2204/BDDDevicesAutomation/commits/main)
# BDDDevicesAutomation

### Overview

* The BDDDevicesAutomation repository is designed for automating tests using Behavior-Driven Development (BDD) with Behave and Selenium, covering web, mobile, and API testing. It’s ideal for developers and testers working on multi-project automation, especially for Chrome, with reusable steps for web UI actions and verifications.

### Why do I need this project?

This project is for chrome

* This project will provide tests specific to performing various browser UI actions and verifications.
* The project will provide the use of the same steps for Web.

### Getting Started
* To use the repository, clone it from GitHub, set up a virtual environment, and install dependencies with pip install -r requirements.txt. Ensure Python 3.x and necessary drivers for Selenium are installed. For IDE setup, consider PyCharm, with guidance at JetBrains PyCharm Download Page.


### How do I get the code, afresh?

* You can download code at https://github.com/lqthang2204/BDDDevicesAutomation
* Clone this project to a working folder on your local machine. Follow https://github.com/lqthang2204/BDDDevicesAutomation for cloning a repository.

### Running Tests
 Run tests using commands like python project_runner.py run -fd 'features/scenarios/web' -tg '{@web}' -fk 3 -sg SIT -pl WEB -ps scenario. Parallel testing is supported with behavex -t @regression --parallel-processes 2, and remote testing with Saucelabs is possible.

### Prerequisites
Before diving in, ensure the following are installed and configured:

* Python: Version 3.x, with 3.9 or higher recommended for compatibility.
* Behave: The BDD framework for Python, essential for running feature files.
* Selenium: Required for browser and device automation, particularly for web and mobile testing.
* Additional Dependencies: Install any other packages listed in the requirements.txt file, which can be done via:

    **pip install -r requirements.txt**
* Device Access: For mobile testing, ensure access to emulators or physical devices, along with necessary drivers.
* IDE: An Integrated Development Environment like PyCharm or VS Code is recommended for development, with setup guidance available at JetBrains PyCharm Download Page.

#### How do I run an automation test?
The repository provides several commands for test execution, detailed in the table above. For example:
* Recommended VM options :
    * Recommended Command for CLI
        * HELP : ```python project_runner.py run --help```
        * RUN  :
            * ```python project_runner.py run -fd 'features/scenarios/web' -tg '{@web}' -fk 3 -sg SIT -pl WEB -ps scenario```
            * ```project_runner.py run -fd 'features/scenarios/web/orange*.feature' -tg '{@test2}' -fk 3 -sg SIT -pl WEB -ps scenario```
            * ```python project_runner.py run -fd features/scenarios/web -tg {@test-2} -fk 3```
    * To run parallel with command
        * ```behavex -t @regression --parallel-processes 2```
        * ```behavex -t @regression --parallel-processes 2 --parallel-scheme scenario```
            * paralle-sheme can have values scenario or feature
            * @regression is the tag in feature files
     * To run remote saucelabs with command
         * ```python project_runner.py run -fd 'features/scenarios/iPhone' -tg '{@scroll_element_ios}' -sg QA -ps scenario -pl IOS -rm true```
         * ```python project_runner.py run -fd 'features/scenarios/android' -tg '{@scroll_element_android}' -sg QA -ps scenario -pl ANDROID -rm true```
         *  ```python project_runner.py run -fd 'features/scenarios/android' -tg '{@scroll_element_android}' -sg QA -ps scenario -pl ANDROID```
         *  default value is false  
     * To execute from a Feature file folder
            * ```behavex -ip features --parallel-processes 2 --parallel-scheme scenario```
                * where -ip features => to include the folder path named features
    * To generate Allure report (if you have Allure package)
        * ```behave -f allure_behave.formatter:AllureFormatter -o allure/results ./features```
        * ```behave -f allure_behave.formatter:AllureFormatter -o allure/results ./features/Login.feature```
        * Sample code you can use to execute in Debug mode is located
          at: ```/Selenium-with-python-behave/launch/Run_Test.py```

----

### How to compose the Feature files ?

- Ensure that you keep 1 line space between the major sections (Feature, Background, Scenario, Scenario Outline) of a
  Feature file

### Tags to be used

    * @final - is a reserved tag and not be used in any feature files. The bdd-tags-processor will filter out the 
               relevant scenario and add @final tag to them 
    *~@norun - can be used to ignore any Feature file or a Scenario
    * ~@ANYTAGNAME - For eg. ~@web will ignore any Feature file or Scenario that has @web tag 

### Config to run

There is scripts use to test in framework

    Given I navigate to "https://www.google.com/"
    And I change the page spec to pageGoogle
    And I wait for element search-field to be DISPLAYED
    And I click element search-field
    And I type "lqthang" into element search-field
    And I navigate to "http://live.techpanda.org/index.php/"
    And I change the page spec to HomePage
    And I wait for element mobile-button to be DISPLAYED
    And I wait for element mobile-button to be ENABLED
    And I wait for element mobile-button to be EXISTED
    And I click element mobile-button
    And I type "test" into element search-input

    Given I navigate to "url"

=> use to open broswer and navigate to URL

    And I change the page spec to pageGoogle

=>use to get element that store in file yaml

And I save text for element pass-field with key "Pass"

=> use to save text of element in web page

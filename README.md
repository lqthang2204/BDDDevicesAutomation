[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flqthang2204%2FSelenium-with-python-behave&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Visitor&edge_flat=false)](https://hits.seeyoufarm.com)
https://github.com/lqthang2204/BDDDevicesAutomation/actions/workflows/project-runner-windows/badge.svg
# BDDDevicesAutomation

### About this project

* The project holds all automation tests for multi-project by browser and mobile (android and ios)

### Why do I need this project?

This project is for chrome

* This project will provide tests specific to performing various browser UI actions and verifications.
* The project will provide the use of the same steps for Web.

### When and why would I need to modify this project?

Any QA or Developer can contribute to this project for valid acceptable scenarios as below:

. Add a new test or feature file of clubbing various tests.
. There is an error with an existing test and needs to be updated.
. There is missing documentation.
. Any other case that should be brought up to QA leads.

### How do I set up Pychamr?

Review the https://www.jetbrains.com/idea/download/#section=windows, which addresses
questions such as:

. How do I import the code into Pycharm?
. How do I check out and change GIT branches?
. What are environment variables and how to configure them for running tests?

### How do I get the code, afresh?

. You can download code at https://github.com/lqthang2204/Selenium-with-python-behave
. Clone this project to a working folder on your local machine.
Follow https://github.com/lqthang2204/Selenium-with-python-behave for cloning a repository.

### Test execution

#### How do I run an automation test?

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

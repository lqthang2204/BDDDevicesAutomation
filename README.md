# Selenium-with-python-behave
:toc: macro
:toclevels: 4
toc::[]
// Automatic Table of contents for github pages only possible with .adoc format
// AsciiDoc format is better format than markdown
// https://asciidoctor.org/docs/asciidoc-vs-markdown/=comparison-by-example

== About this project
* The project holds all automation tests for multi project by browser


== Why do I need this project?
This project is for multi browser (chrome)

* This project will provide tests specific to performing various browser UI actions and verifications.
* The project will provide use of the same steps for Web.

== When and why would I need to modify this project?
Any QA or Developer can contribute to this project for valid acceptable scenarios as below:

. Add a new test or feature file of clubbing various tests.
. There is an error with an existing test and needs to be updated.
. There is missing documentation.
. Any other case that should be brought up to QA leads.

== How do I setup Pychamr?
Review the https://www.jetbrains.com/idea/download/#section=windows, which addresses
questions such as:

. How do I import the code into Pycharm?
. How do I check out and change GIT branches?
. What are environment variables and how to configure them for running tests?

== How do I get the code, afresh?
. You can download code at https://github.com/lqthang2204/Selenium-with-python-behave
. Clone this project to a working folder on your local machine.
Follow https://github.com/lqthang2204/Selenium-with-python-behave for cloning a repository.

== Test execution

=== How do I run a automation test?
. VM options : behave ./features/orangeHRM.feature
to run parallel with command behavex -t @TAGS regression --parallel-processes 2
with regression is the tag in file feature

----



Config to run

there is scripts use to test in framework

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
=> use to open broswer and navigate to url

    And I change the page spec to pageGoogle
=>use to get element that store in file yaml


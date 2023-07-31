@misc-operations
Feature: Numerical, String Compare and Math Calculations

  @numerical
  Scenario: Perform Numerical comparison
    Given I perform operations with below attributes
      | Left | Operator              | Right | SaveAs         |
      | 11   | greater-than          | 4     | GreaterThan114 |
      | 11   | greater-than-equal-to | 4     |                |
      | 3    | less-than             | 4     | LessThan114    |
      | 5    | less-than-equal-to    | 5     |                |
      | 11   | equal-to              | 11    |                |
      | 11   | not-equal-to          | 4     |                |
    And I print all the dictionary keys

  @string
  Scenario: Perform String comparison
    Given I perform operations with below attributes
      | Left  | Operator       | Right   | SaveAs        |
      | hello | contains       | ell     | Containshello |
      | HELLO | case-match     | HELLO   |               |
      | HELLO | ignore-case    | hello   |               |
      | apple | does-not-match | oranges | DoesntMatch   |
    And I print all the dictionary keys

  @compare
  Scenario: Perform String comparison - using Keys
    Given I create a set of keys with below attributes
      | Pattern to create data from | Save into Key Name |
      | random_alphabet_5           | randomAplhabetLen5 |
    Given I perform operations with below attributes
      | Left                   | Operator       | Right | SaveAs |
      | HELLO                  | case-match     | HELLO |        |
      | 15                     | equal-to       | 15    |        |
      | 14                     | not-equal-to   | 15    |        |
      | 14                     | does-not-match | 15    |        |
      | randomAplhabetLen5     | does-not-match | 15    |        |
      | KEY.randomAplhabetLen5 | does-not-match | 15    |        |

  @string-failing
  Scenario: Perform String comparison - failing Tests
    Given I create a set of keys with below attributes
      | Pattern to create data from | Save into Key Name |
      | random_alphabet_5           | randomAplhabetLen5 |
    Given I perform operations with below attributes
      | Left               | Operator | Right     | SaveAs |
      | randomAplhabetLen5 | contains | test-this |        |

  @calculations
  Scenario: Perform calculations on number
    Given I perform operations with below attributes
      | Left | Operator | Right | SaveAs      |
      | 5    | add      | 4     | AddNums     |
      | 11   | subtract | 4     | SubTractNum |
      | 20   | divide   | 4     | DivideNum   |
      | 5    | multiply | 4     | MultiplyNum |
    And I print all the dictionary keys

  @calculations
  Scenario: Perform concatenation on string
    Given I perform operations with below attributes
      | Left   | Operator | Right | SaveAs       |
      | hello_ | concat   | user  | Concatenated |
    And I print all the dictionary keys

  @norun
  Scenario: Incorrect Implementation
    Given I create a set of keys with below attributes
      | Pattern to create data from | Save into Key Name |
      | random_alphabet_5           | randomAplhabetLen5 |
    Given I perform operations with below attributes
      | Left               | Operator | Right     | SaveAs |
      | randomAplhabetLen5 | equal-to | test-this |        |
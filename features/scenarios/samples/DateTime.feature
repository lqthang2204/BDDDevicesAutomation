@datetime
Feature: How to get Data Time random data

  @dates
  Scenario: Get Random Date Time Data
    Given I create a set of keys with below attributes
      | Pattern to create data from | Save into Key Name       |
      | date_current_yyyy-MM-dd     | FormatedDate1            |
      | date_+3dt_yyyy-MM-dd        | FormatedDate2            |
      | date_+3dt_yyyy/MM/dd        | FormatedDate3            |
      | date_+3dt_dd/MM/yyyy        | FormatedDate4            |
      | date_+3dt_yyyy/dd/MM/       | FolderPathDateStampt     |
      | dateTime_current            | currentDateTime          |
      | dateTime_current_UTC        | currentDateTimeUTC       |
      | dateTime_+1yr_UTC           | DateTimeUTC_nextYr       |
      | dateTime_+1mo_UTC           | DateTimeUTC_nextMonth    |
      | dateTime_+1wk_UTC           | DateTimeUTC_nextWeek     |
      | dateTime_+1800sc_UTC        | DateTimeUTC_After1800Sec |
      | dateTime_-30mi_UTC          | DateTimeUTC_before30Mins |
      | dateTime_-1dt               | yesterdayDateTime        |
      | dateTime_-1dt_CET           | yesterdayDateTimeCET     |
      | dateTime_-1dt_CET           | yesterdayDateTimeCET     |
      | date_current                | currentDate              |
      | date_current_UTC            | currentDateUTC           |
      | date_+1dt                   | tomorrowDate             |
      | time_current                | currentTime              |
      | time_+2hr                   | timeAfter2Hr             |
      | time_-25mi_hh:mm            | timeBefore25MinsHHMM     |
      | time_+2hr_hh:mm             | timeAfter2HrHHMM         |
      | time_-25mi                  | timeBefore25Mins         |
      | date_current_year           | current_year             |
      | date_+1yr_year              | nextYear                 |
      | date_+3dt_dayOfWeek         | dayOfWeek+3              |
      | date_current_dayOfWeek      | currentdayOfWeek         |
      | time_current_UTC            | timeUTC                  |
    And I print all the dictionary keys

  @numbers
  Scenario: Get Random Number Data
    Given I create a set of keys with below attributes
      | Pattern to create data from             | Save into Key Name      |
      | random_alphabet_5                       | randomAplhabetLen5      |
      | random_alphabet_10                      | randomAplhabetLen10     |
      | random_alphabet_5-8                     | randomAplhabetRange     |
      | random_alphanumeric_7                   | randomAplhaNumericLen   |
      | random_alphanumeric_8-12                | randomAplhaNumericRange |
      | random_number_3                         | randomIntLen            |
      | random_number_3-5                       | randomIntRange          |
      | random_number_3.random_number_2         | randomPrice1D           |
      | random_number_10-15.random_number_10-15 | randomPrice2D           |
    And I print all the dictionary keys
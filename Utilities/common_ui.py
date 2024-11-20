import logging
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from faker import Faker
from selenium.common import NoSuchElementException, NoSuchFrameException, NoSuchWindowException, \
    StaleElementReferenceException, ElementNotInteractableException, InvalidElementStateException, \
    ElementNotVisibleException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Utilities.action_android import ManagementFileAndroid
from Utilities.action_web import ManagementFile
from project_runner import logger
from selenium.webdriver.support.color import Color
from libraries.data_generators import check_match_pattern, get_test_data_for
import copy
import re
from selenium.webdriver.support.ui import Select
from Utilities.process_value_input import procees_value


class common_device:
    count_number = 0

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def action_page(self, element_page, action, driver, value, wait, dict_save_value, device, context, count_number=0):
        """
           Executes a specified action on a given element.

           Args:
               element_page (dict): Element details such as locator strategy and value.
               action (str): The action to perform (e.g., 'click', 'type').
               driver (WebDriver): Selenium WebDriver instance.
               value (str): Value to use for certain actions (e.g., typing).
               wait (WebDriverWait): Explicit wait object.
               dict_save_value (dict): Context dictionary for dynamic value processing.
               device (str): Target device context.
               context (object): Test context with configurations like highlighting.
               count_number (int): Retry count for handling exceptions.
           """
        try:
            # Locate the element on the device
            element = self.get_element_by_from_device(element_page, device, driver)
            logger.info(f'Executing {action} on element with value: {element_page["value"]}')
            # Highlight the element for better visibility during testing
            self.highlight(element, 0.3, context.highlight)
            if value:
                value = procees_value().get_value(value, dict_save_value)
                value = get_test_data_for(value, dict_save_value)
            # Define a map of actions to corresponding methods
            actions_map = {
                "click": lambda: self.click_action(element, wait, element_page, device, driver),
                "double-click": lambda: ActionChains(driver).double_click(on_element=element).perform(),
                "right-click": lambda: ActionChains(driver).context_click(on_element=element).perform(),
                "select": lambda: Select(element).select_by_visible_text(value),
                "type": lambda: element.send_keys(value),
                "text": lambda: element.send_keys(value),
                "clear": lambda: element.clear(),
                "hover-over": lambda: self.mouse_action(element, driver, action, device),
                "scroll": lambda: self.scroll_to_element(element, driver, False, device, False),
            }
            # Perform the action if supported
            if action in actions_map:
                actions_map[action]()
            else:
                logger.error(f"Unsupported action: {action}")
                assert False, f"Action '{action}' is not supported in the framework"
        except (ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException):
            # Handle known interaction exceptions
            self.handle_element_not_interactable_exception(
                element_page, action, driver, value, wait, dict_save_value, device, context, count_number)
        except InvalidElementStateException:
            # Handle invalid state exceptions
            self.handle_invalid_element_state_exception(value, element_page, device, driver, action)
        except Exception as e:
            # Log and raise any other exceptions
            logger.error(f"Error performing '{action}' on element '{element}': {str(e)}")
            raise

    def click_action(self, element, wait, element_page, device, driver):
        """
           Handles click actions for elements based on the device type (WEB or MOBILE).

           Args:
               element (WebElement): The target element to click.
               wait (int): Maximum wait time for conditions.
               element_page (dict): Element details including device, type, and value.
               device (str): Target device context ('WEB' or 'MOBILE').
               driver (WebDriver): Selenium WebDriver instance.
           """
        try:
            if element_page['device'] == "WEB":
                # Check if the element is not disabled
                if element.get_attribute("disabled") is None:
                    logger.info("Element is enabled. Performing click.")
                    element.click()
                else:
                    # Wait until the element is no longer disabled
                    logger.info("Element is disabled. Waiting for it to become enabled.")
                    WebDriverWait(driver, wait).until_not(
                        ec.element_attribute_to_include(
                            ManagementFile().get_locator_for_wait(element_page['type'], element_page['value']),
                            "disabled"))
                    logger.info("Element is now enabled. Performing click.")
                    element.click()
            # For MOBILE elements
            else:
                logger.info(f"Clicking element on {device} device.")
                # Wait until the element is clickable
                locator_from_wait = ManagementFileAndroid().get_locator_for_wait(element_page['type'],
                                                                                 element_page['value'])
                WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator_from_wait))
                element.click()
                logger.info(f"Click action successfully performed on element: {element_page['value']}")
        except Exception as e:
            # Log the error and raise the exception
            logger.error(f"Error during click action on element: {element_page['value']}. Error: {str(e)}")

    def wait_element_for_status(self, element_page, status, driver, device, wait, flag):
        """
        Waits for an element to have a specific status.

        Args:
            element_page (dict): The element page specification.
            status (str): The desired status of the element.
            driver (WebDriver): The Selenium WebDriver instance.
            device (dict): The device information.
            wait (int): The wait time in seconds.
            flag (bool): Determines if the test should skip or fail on failure.

        Returns:
            str: "PASS" if the element achieved the desired status, otherwise "SKIP" if `flag` is True.

        Raises:
            AssertionError: If the element does not achieve the expected status and `flag` is False.
            ValueError: If the status is not supported.
        """
        # Get the locator for waiting
        locator_from_wait = self.get_locator_for_wait_from_device(element_page)
        logger.info(f"Waiting for element '{element_page['value']}' to have status '{status}'")

        try:
            # Status mapping for WebDriverWait conditions
            status_map = {
                "DISPLAYED": lambda: WebDriverWait(driver, wait).until(
                    ec.visibility_of_element_located(locator_from_wait)),
                "NOT_DISPLAYED": lambda: WebDriverWait(driver, wait).until(
                    ec.invisibility_of_element_located(locator_from_wait)),
                "ENABLED": lambda: WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator_from_wait)),
                "NOT_ENABLED": lambda: WebDriverWait(driver, wait).until_not(
                    ec.element_to_be_clickable(locator_from_wait)),
                "EXISTED": lambda: WebDriverWait(driver, wait).until(lambda _: len(
                    self.get_list_element_by_from_device(element_page, device, driver)) > 0),
                "NOT_EXISTED": lambda: WebDriverWait(driver, wait).until(lambda _: len(
                    self.get_list_element_by_from_device(element_page, device, driver)) == 0),
                "SELECTED": lambda: WebDriverWait(driver, wait).until(
                    ec.element_located_to_be_selected(locator_from_wait)),
                "NOT_SELECTED": lambda: WebDriverWait(driver, wait).until_not(
                    ec.element_located_to_be_selected(locator_from_wait)),
            }

            # Execute the condition for the specified status
            if status in status_map:
                status_map[status]()
            else:
                raise ValueError(f"Unsupported status: {status}")

            logger.info(f"Element '{element_page['value']}' successfully achieved status '{status}'")
            return "PASS"

        except Exception as e:
            # Log the error
            logger.error(f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}")
            # Handle test flow based on the `flag`
            assert flag, f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}"
            if flag:
                return "SKIP"

    def get_element(self, page, element, platform_name, dict_save_value):
        """
        Retrieves the locator for a given element from a page specification.

    Args:
        page (dict): The page specification containing element locators.
        element (str): The ID of the element to retrieve the locator for.
        platform_name (str): The platform for which the locator is needed (e.g., 'iOS', 'Android').
        dict_save_value (dict): A dictionary of values to be used for substitution in the locator.

    Returns:
        dict: The locator for the given element, after applying necessary text substitutions.

    Raises:
        ValueError: If the element or its locator for the specified platform is not found.
        TypeError: If inputs are of incorrect types.
        """
        # Validate inputs
        self._validate_get_element_inputs(page, element, platform_name, dict_save_value)

        text = ""

        # Check if the element has a text condition
        if "with text" in element:
            element, text = self._extract_text_from_element(element, dict_save_value)

        # Find the element in the page specification
        element_spec = self._find_element_in_page(page, element, platform_name)

        # Retrieve the locator for the specified platform
        locator = self._find_locator_for_platform(element_spec, platform_name)

        # Substitute the text in the locator value if applicable
        if "{text}" in locator['value'] and text:
            logger.info(f"Substituting '{text}' into locator value: {locator['value']}")
            locator_temp = copy.deepcopy(locator)
            locator_temp['value'] = locator_temp['value'].replace("{text}", text)
            return locator_temp
        return locator

    def _validate_get_element_inputs(self, page, element, platform_name, dict_save_value):
        """
        Validates inputs for the get_element method.

        Args:
            page (dict): The page specification.
            element (str): The element ID.
            platform_name (str): The platform name.
            dict_save_value (dict): Dictionary of saved values.

        Raises:
            ValueError or TypeError: If validation fails.
        """
        if not isinstance(page, dict):
            raise TypeError("Expected 'page' to be a dictionary.")
        if not isinstance(element, str) or not element:
            raise ValueError("Element ID should be a non-empty string.")
        if not isinstance(platform_name, str) or not platform_name:
            raise ValueError("Platform name should be a non-empty string.")
        if dict_save_value is not None and not isinstance(dict_save_value, dict):
            raise TypeError("Expected 'dict_save_value' to be a dictionary or None.")
    def _extract_text_from_element(self, element, dict_save_value):
        """
        Extracts and processes the text condition from the element ID if present.

    Args:
        element (str): The element ID potentially containing a 'with text' condition.
        dict_save_value (dict): A dictionary for substituting dynamic text values.

    Returns:
        tuple: A tuple containing the processed element ID (str) and the associated text (str).

    Raises:
        ValueError: If the 'with text' format is malformed or missing necessary parts.
        """
        # Split the element by 'with text' and strip any excess whitespace
        arr_value = [i.strip() for i in element.split("with text", maxsplit=1)]
        element = arr_value[0]  # Element ID without text condition
        if len(arr_value) > 1:  # Check if 'with text' exists
            text = arr_value[1].replace('"', '').strip()  # Remove quotes and extra spaces
            if not text:
                raise ValueError("Text condition after 'with text' is empty or invalid.")

        # If a dictionary of values is provided, substitute the text
        if dict_save_value and text in dict_save_value:
            substituted_text = dict_save_value.get(text)
            logger.info(f"Substituted '{text}' with '{substituted_text}' from dict_save_value.")
            text = substituted_text
        else:
            logger.warning(f"Text '{text}' not found in dict_save_value; using as-is.")
        logger.info(f"Extracted element ID: '{element}', text: '{text}'")
        return element, text

    def _find_element_in_page(self, page, element, platform_name):
        """
        Finds the element in the page specification.

        Args:
            page (dict): The page specification.
            element (str): The ID of the element.
            platform_name (str): The platform name (for logging purposes).

        Returns:
            dict: The element specification if found.

        Raises:
            ValueError: If the element is not found in the page specification.
        """
        element_spec = next((el for el in page['elements'] if el['id'] == element), None)
        if element_spec is None:
            logger.error(f"Element '{element}' not found in page spec for platform '{platform_name}'.")
            raise ValueError(f"Element '{element}' not found in page spec for platform '{platform_name}'.")

        return element_spec

    def _find_locator_for_platform(self, element_spec, platform_name):
        """
        Finds the locator for the specified platform from the element specification.

        Args:
            element_spec (dict): The element specification containing locators.
            platform_name (str): The platform name (e.g., 'iOS', 'Android').

        Returns:
            dict: The locator for the specified platform.

        Raises:
            ValueError: If the locator for the platform is not found.
        """
        locator = next((loc for loc in element_spec['locators'] if loc['device'] == platform_name), None)
        if locator is None:
            logger.error(f"Locator for element '{element_spec['id']}' not found for platform '{platform_name}'.")
            raise ValueError(f"Locator for element '{element_spec['id']}' not found for platform '{platform_name}'.")

        return locator

    def verify_elements_with_status(self, page, table, platform_name, dict_save_value, driver, device, wait):
        """
           This function verifies the status of elements in a given page.
           Args:
               page (dict): The page specification.
               table (list): The table containing the elements to verify.
               platform_name (str): The platform for which the elements are needed.
               dict_save_value (dict): A dictionary of values to be used for substitution in the elements.
               driver (WebDriver): The Selenium WebDriver instance.
               device (dict): The device information.
               wait (WebDriverWait): The WebDriverWait instance.
           Raises:
               AssertionError: If the table is not set for elements.
           """
        if table:
            for row in table:
                arr_element = page['elements']
                arr_element = list(filter(
                    lambda element: element['id'] == row["Field"], arr_element
                ))
                logger.info(f'Verifying for {row["Field"]} have value {row["Value"]} and status {row["Status"]}')
                value = row["Value"]
                value = procees_value().get_value(value, dict_save_value)
                if value:
                    element_yaml = self.get_element(page, arr_element[0]['id'] + " with text " + value, platform_name,
                                                dict_save_value)
                else:
                    element_yaml = self.get_element(page, arr_element[0]['id'], platform_name,
                                                    dict_save_value)
                self.wait_element_for_status(element_yaml, row["Status"], driver, device, wait, False)
                logger.info(f'Verified for {row["Field"]} have value {row["Value"]} and status {row["Value"]}')
        else:
            logger.error("user must set data table for elements")
            assert False, "can not execute verify status for elements"

    def save_text_from_element(self, element_page, driver, key, dict_save_value, wait, device, is_regex, pattern):
        """
            Save the text from an element on a web page.
            Args:
                element_page (dict): The specification of the element on the page.
                driver (WebDriver): The Selenium WebDriver instance.
                key (str): The key to save the text value under in the dictionary.
                dict_save_value (dict): The dictionary to save the text value in.
                wait (int): The wait time in seconds.
                device (dict): The device information.
            Returns:
                dict: The updated dictionary with the saved text value.
            Raises:
                AssertionError: If the wait fails or if the element is not found.
            """
        try:
            # Get the locator for waiting
            locator_from_wait = self.get_locator_for_wait_from_device(element_page)

            # Log the wait action
            logger.info(f"Saving text for element '{element_page['value']}' with key '{key}'")

            # Wait for the element to be present
            WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator_from_wait))

            # Get the element
            element = self.get_element_by_from_device(element_page, device, driver)

            # Scroll to the element if needed
            self.scroll_to_element_by_js(element, driver, True, device['platformName'], True)

            # Get the value of the element
            value = self.get_value_element_form_device(element, device, element_page, driver)
            if is_regex:
                value = re.search(pattern, value).group(1)
            # Save the value to the dictionary
            dict_save_value["KEY." + key] = value

            return dict_save_value
        except Exception as e:
            # Log the error if the wait fails
            logger.error(f"Failed to save text for element '{element_page['value']}' with key '{key}': {str(e)}")
            raise AssertionError(f"Failed to save text for element '{element_page['value']}' with key '{key}'") from e

    def get_locator_for_wait_from_device(self, element_page):
        """
           Get the locator for waiting based on the device platform.
           Args:
               element_page (dict): The element page specification.
               device (dict): The device information.
           Returns:
               tuple: The locator for waiting.
           """
        # Check if the device platform is WEB
        if element_page['device'] == "WEB":
            return ManagementFile().get_locator_for_wait(element_page['type'], element_page['value'])
        elif element_page['device'] == "ANDROID" or element_page['device'] == "IOS":
            return ManagementFileAndroid().get_locator_for_wait(element_page['type'], element_page['value'])
        else:
            raise ValueError("Unknown device platform: {}".format(element_page['device']))

    def get_list_element_by_from_device(self, element_page, device, driver):
        if device['platformName'] == "WEB":
            return ManagementFile().get_list_element_by(element_page['type'], driver, element_page['value'])
        elif device['platformName'] == "ANDROID" or device['platformName'] == "IOS":
            return ManagementFileAndroid().get_list_element_by(element_page['type'], driver, element_page['value'])
        else:
            raise ValueError("Unknown device platform: {}".format(device['platformName']))

    def get_element_by_from_device(self, element_page, device, driver):
        if element_page['device'] == "WEB":
            return ManagementFile().get_element_by(element_page['type'], driver, element_page['value'])
        elif element_page['device'] == "ANDROID" or element_page['device'] == "IOS":
            return ManagementFileAndroid().get_by_android(element_page['type'], driver, element_page['value'])
        else:
            raise ValueError("Unknown device platform: {}".format(device['platformName']))

    def get_value_element_form_device(self, element, device, element_page, driver):
        """
            Returns the value of the element based on the platform.
            Args:
                element: The element to retrieve the value from.
                device: The device platform information.
            Returns:
                The value of the element based on the platform.
            """
        if device['platformName'] == "WEB":
            # Check if the element has a value attribute and is an input tag
            try:
                if element.get_attribute("value") and element.tag_name.lower() == "input":
                    logger.info("Getting text on element: ")
                    return element.get_attribute('value')
                else:
                    # If the element is not an input tag, return its text content
                    text = element.text
                    if len(text) == 0:
                        text = element.get_attribute('innerText')
                        return text
                    if len(text) != 0:
                        logger.info("Text on element: " + text)
                        return text

            except (ElementNotInteractableException, StaleElementReferenceException):
                sleep(2)
                element = self.get_element_by_from_device(element_page, device, driver)
                self.get_value_element_form_device(element, device, element_page, driver)

        else:
            # For non-web platforms, return the element's text content
            return element.text
        self.count_number = 0

    def get_value_attribute_element_form_device(self, element, device, value, flag):
        """
            Returns the value of the specified attribute of the element based on the platform.

            Args:
                element: The element to retrieve the attribute value from.
                device: The device platform information.
                value: The name of the attribute to retrieve.
                flag: A flag indicating whether to retrieve the value using CSS property or attribute.

            Returns:
                The value of the specified attribute of the element based on the platform.

            Raises:
                ValueError: If the device platform is not supported.
            """
        if device['platformName'] == "WEB":
            if flag:
                value_attribute = element.value_of_css_property(value)
                if 'color' in value:
                    return Color.from_string(value_attribute).hex.lower()
                else:
                    return value_attribute.lower()
            else:
                return element.get_attribute(value)
        elif device['platformName'] == "ANDROID" or device['platformName'] == "IOS":
            return element.get_attribute(value)
        else:
            raise ValueError("Unknown device platform: {}".format(device['platformName']))

    def create_random_user(self, locale: str) -> dict:
        """
        Create a random user with fake data.

        Args:
            locale (str): The locale to use for generating the fake data.

        Returns:
            dict: A dictionary containing the generated user data.

        Raises:
            ValueError: If the provided locale is not supported.

        """
        # Create a Faker instance based on the provided locale or use the default 'en_US'
        if locale:
            faker = Faker(locale)
        else:
            faker = Faker('en_US')

        # Log the generated first name
        logger.info(f'faker.unique.first_name() == {faker.unique.first_name()}')

        # Generate the user data using the Faker instance
        user = {
            'first_name': faker.unique.first_name(),
            'last_name': faker.unique.last_name(),
            'middle_name': faker.unique.first_name_male(),
            'job': faker.job(),
            'address': faker.address(),
            'phone_number': faker.phone_number(),
            'city': faker.city(),
            'state': faker.state(),
            'postcode': faker.postcode(),
            'domain_name': faker.domain_name(),
            'prefix': faker.prefix(),
            'suffix': faker.suffix(),
            'email': faker.unique.email()
        }
        return user

    def verify_elements_below_attributes(self, page, row, platform_name, dict_save_value, driver, device, wait,
                                         is_highlight, page_present):
        """
        Verify the attributes of elements in a given page.

        Args:
            page (dict): The page specification.
            row (list): The row containing the element attributes to verify.
            platform_name (str): The platform for which the elements are needed.
            dict_save_value (dict): A dictionary of values to be used for substitution in the elements.
            driver (WebDriver): The Selenium WebDriver instance.
            device (dict): The device information.
            wait (WebDriverWait): The WebDriverWait instance.
            is_highlight (bool): Whether to highlight the element.

        Raises:
            AssertionError: If the element is not found or the status does not match.


        """
        arr_element = page['elements']
        arr_element = list(filter(
            lambda element: element['id'] == row[0], arr_element
        ))
        if not arr_element:
            logger.error(f'Element with ID {row[0]} not found in the page {page_present}.yaml')
            assert False, f'Element with ID {row[0]} not found in the page'

        logger.info(f'Verifying for {row[0]} have value {row[1]} and status {row[2]}')
        value = row[1]
        helper = row[3]
        if value is None:
            value = ''
        else:
            value = procees_value().get_value(value, dict_save_value)

        element_yaml = self.get_element(page, arr_element[0]['id'], platform_name,
                                        dict_save_value)
        if not element_yaml:
            raise AssertionError(f'Element with ID {row[0]} and value {value} not found in the page')

        if row[2] and element_yaml:
            if value != '' and helper is None:
                logger.info(f'Verified for {row[0]} have value {row[1]} and status {row[2]}')
                self.wait_element_for_status(element_yaml, row[2], driver, device, wait, False)
                self.verify_value_in_element(element_yaml, value, device, driver, is_highlight, wait)
            else:
                logger.info(f'Verified for {row[0]} have value {row[1]} and status {row[2]}')
                self.wait_element_for_status(element_yaml, row[2], driver, device, wait, False)
        else:
            raise AssertionError('Table must contain both field name and status')

        self.verify_value_with_helpers(value, helper, element_yaml, device, driver, is_highlight)

    # def get_value_from_user_random(self, value, dict_save_value):
    #     try:
    #         if 'USER.' not in dict_save_value:
    #             raise KeyError("'USER.' key not found in dict_save_value")
    #
    #         arr_user = value.split('USER.')
    #         list_user = dict_save_value['USER.']
    #         if len(arr_user) < 2:
    #             raise ValueError("Invalid format for value. Expected 'USER.' followed by a key.")
    #         value = management_user.get_user(list_user, arr_user[1])
    #         logging.info(f"Value '{value}' retrieved successfully for key '{arr_user[1]}'")
    #         return value
    #     except KeyError as ke:
    #         logging.error(f"KeyError: {ke}")
    #         raise
    #     except ValueError as ve:
    #         logging.error(f"ValueError: {ve}")
    #         raise
    #     except Exception as e:
    #         logging.error(f"An error occurred: {e}")
    #         raise

    def verify_value_in_element(self, element_page, expect, device, driver, is_highlight, wait):
        try:
            locator_from_wait = common_device().get_locator_for_wait_from_device(element_page)
            WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator_from_wait))
            element = self.get_element_by_from_device(element_page, device, driver)
            self.scroll_to_element_by_js(element, driver, True, device['platformName'], is_highlight)
            value = self.get_value_element_form_device(element, device, element_page, driver)
            logger.debug(f'value of the element is "{value}"')
            logger.debug(f'values expected "{expect}"')
            assert value == expect, f'value of the element is "{value}" not equal to values expected "{expect}"'
        except NoSuchElementException:
            logger.error('Element not found')
            assert False, 'Element not found'

    def verify_value_with_helpers(self, expected, helper, element_page, device, driver, is_highlight):
        if helper in ['BACKGROUND-COLOR', 'COLOR', 'FONT_FAMILY', 'FONT_SIZE', 'FONT_WEIGHT', 'FONT_HEIGHT',
                      'TEXT_ALIGN'] and expected and device['platformName'] != 'WEB':
            assert False, f'framework only check {helper} for WEB env, not support for native app'
        if helper and expected:
            element = self.get_element_by_from_device(element_page, device, driver)
            self.scroll_to_element_by_js(element, driver, True, device['platformName'], is_highlight)
            if helper == 'REGEX':
                value_element = self.get_value_element_form_device(element, device, element_page, driver)
                check_match_pattern(expected, value_element, 'value of element not match with pattern')
            elif helper == 'STARTS_WITH':
                value_element = self.get_value_element_form_device(element, device, element_page, driver)
                assert value_element.startswith(expected), f'value of element is {expected} not start with {expected}'
            elif helper == 'ENDS_WITH':
                value_element = self.get_value_element_form_device(element, device, element_page, driver)
                assert value_element.endswith(expected), f'value of element is {expected} not ends with {expected}'
            elif helper == 'CONTAINS':
                value_element = self.get_value_element_form_device(element, device, element_page, driver)
                assert expected in value_element, f'value of element is {value_element} not contains {expected}'
            elif helper == 'BACKGROUND-COLOR':
                bg_color = self.get_value_attribute_element_form_device(element, device, 'background-color', True)
                assert bg_color == expected.lower(), f'element there is no background color same with {expected}'
            elif helper == 'COLOR':
                color = self.get_value_attribute_element_form_device(element, device, 'color', True)
                assert color == expected.lower(), f'element there is no color same with {expected}'
            elif helper == 'FONT_FAMILY':
                value_attribute = self.get_value_attribute_element_form_device(element, device, 'font-family', True)
                assert value_attribute == expected.lower(), f'element there is no font family same with {expected}'
            elif helper == 'FONT_SIZE':
                value_attribute = self.get_value_attribute_element_form_device(element, device, 'font-size', True)
                assert value_attribute == expected.lower(), f'font family of element not same with {expected}'
            elif helper == 'FONT_WEIGHT':
                value_attribute = self.get_value_attribute_element_form_device(element, device, 'font-weight', True)
                assert value_attribute == expected.lower(), f'font weight of element not same with {expected}'
            elif helper == 'FONT_HEIGHT':
                value_attribute = self.get_value_attribute_element_form_device(element, device, 'height', True)
                assert value_attribute == expected.lower(), f'font height of element not same with {expected}'
            elif helper == 'TEXT_ALIGN':
                value_attribute = self.get_value_attribute_element_form_device(element, device, 'text-align', True)
                assert value_attribute == expected.lower(), f'font align of element not same with {expected}'
            else:
                value_attribute = self.get_value_attribute_element_form_device(element, device, helper, False)
                assert value_attribute == expected, f'value attribute of element not same with {expected}, need to check attribute of element'
        elif helper and expected == '':
            logger.error('The helper and value columns must both contain a value simultaneously.')
            assert False, f'The helper and value columns must both contain a value simultaneously.  helper = {helper}, value = {expected}'

    def highlight(self, element, time, is_hightlight):
        """
          Highlights (blinks) a Selenium Webdriver element for a specified time.

          Args:
              element: The Selenium Webdriver element to highlight.
              time: The duration in seconds to highlight the element.
              is_highlight: Flag to determine if highlighting should be applied.

          Returns:
              None
          """
        if is_hightlight == 'true':
            try:
                driver = element._parent

                def apply_style(s):
                    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                                          element, s)

                original_style = element.get_attribute('style')
                apply_style("background: yellow; border: 2px solid red;")
                sleep(float(time))
                apply_style(original_style)
            except Exception as e:
                pass

    def mouse_action(self, element, driver, action, device):
        if action == 'hover-over':
            if device['platformName'] == 'WEB':
                action = ActionChains(driver)
                action.move_to_element(element).perform()
            else:
                action = TouchAction(driver)
                action.press(element).release().perform()

    def scroll_to_element_by_js(self, element, driver, flag, platform, is_highlight):
        """
          Scrolls to the specified Selenium Webdriver element using JavaScript.

          Args:
              element: The Selenium Webdriver element to scroll to.
              driver: The WebDriver instance.
              flag: A flag indicating whether scrolling was successful.
              platform: The platform name.
              is_highlight: Flag to determine if highlighting should be applied.

          Returns:
              None
          """
        if platform == 'WEB':
            try:
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", element)
                self.highlight(element, 0.3, is_highlight)
            except:
                assert flag, f'can not scroll to element {element}'
        else:
            assert True, f'feature scroll to element by javascript only support for Web environment'

    def scroll_to_element(self, element, driver, flag, platform, is_highlight):
        """
           Scroll to the specified element on the webpage.

           Args:
               element: The Selenium Webdriver element to scroll to.
               driver: The WebDriver instance.
               platform: The platform name (default is 'WEB').
               is_smooth_scroll: Flag to enable smooth scrolling (default is True).

           Returns:
               None
           """
        if platform == 'WEB':
            try:
                ActionChains(driver).scroll_to_element(element).perform()
                self.highlight(element, 0.3, is_highlight)
            except:
                try:
                    logger.info(f'can not scroll to element {element} trying to scroll by javascript')
                    self.scroll_to_element_by_js(element, driver, flag, platform, is_highlight)
                except:
                    assert flag, f'can not scroll to element {element}'

    def switch_to_frame(self, driver, element_page, wait, device, status):
        try:
            if status:
                WebDriverWait(driver, wait).until(ec.frame_to_be_available_and_switch_to_it(
                    ManagementFile().get_locator_for_wait(element_page['type'], element_page['value'])))
            else:
                driver.switch_to.default_content()
        except NoSuchElementException as e:
            print(f'Frame element not found: {e}')
        except Exception as e:
            print(f'Failed to switch to frame: {e}')

    def switch_to_frame_by_index(self, driver, index):
        try:
            driver.switch_to.frame(int(index))
        except NoSuchFrameException as e:
            print(f'Frame with index {index} not found: {e}')
        except Exception as e:
            print(f'Failed to switch to frame with index {index}: {e}')
        except IndexError as e:
            print(f'Index must be integer {index}: {e}')

    def switch_to_tab_by_index(self, driver, index):
        """
        Switches to the tab at the specified index in a Selenium Webdriver session.

        Args:
            driver: The WebDriver instance.
            index: The index of the tab to switch to.

        Returns:
            None
        """
        try:
            driver.switch_to.window(driver.window_handles[int(index) - 1])
        except IndexError as e:
            print(f'Tab with index {index} not found: {e}')
        except Exception as e:
            print(f'Failed to switch to tab with index {index}: {e}')

    def switch_to_tab_by_title(self, driver, title):
        """
        Switches to the tab with the specified title in a Selenium Webdriver session.

        Args:
            driver: The WebDriver instance.
            title: The title of the tab to switch to.

        Returns:
            None
        """
        try:
            all_handles = driver.window_handles
            for handle in all_handles:
                driver.switch_to.window(handle)
                if driver.title == title:
                    break
            else:
                raise NoSuchWindowException(f"Tab with title '{title}' not found")
        except NoSuchWindowException as e:
            print(f'Tab with title "{title}" not found: {e}')
        except Exception as e:
            print(f'Failed to switch to tab with title "{title}": {e}')

    def close_web_page(self, driver, title):
        tab_list = driver.window_handles
        flag = False
        for tab in tab_list:
            driver.switch_to.window(tab)
            if driver.title == title:
                driver.close()
                flag = True
                break
        assert flag, f'can not close to tab has {title}, please verify title in page'

    def close_by_index(self, driver, index):
        """
           Closes the tab at the specified index in a Selenium Webdriver session.

           Args:
               driver: The WebDriver instance.
               index: The index of the tab to close.

           Returns:
               None
           """
        try:
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[int(index) - 1])
            driver.close()
            # Switch back to the main window if needed
            driver.switch_to.window(all_handles[0])
        except IndexError as e:
            print(f'Tab with index {index} not found: {e}')
        except Exception as e:
            print(f'Failed to close tab with index {index}: {e}')

            # list key board  NULL = "\ue000", CANCEL = "\ue001"  # ^break,HELP = "\ue002",BACKSPACE = "\ue003",BACK_SPACE = BACKSPACE,TAB = "\ue004",CLEAR = "\ue005",RETURN = "\ue006",ENTER = "\ue007",SHIFT = "\ue008",LEFT_SHIFT = SHIFT,CONTROL = "\ue009",LEFT_CONTROL = CONTROL,ALT = "\ue00a",LEFT_ALT = ALT,PAUSE = "\ue00b",ESCAPE = "\ue00c",SPACE = "\ue00d",PAGE_UP = "\ue00e",PAGE_DOWN = "\ue00f",END = "\ue010",HOME = "\ue011",LEFT = "\ue012",ARROW_LEFT = LEFT,UP = "\ue013",ARROW_UP = UP,RIGHT = "\ue014",ARROW_RIGHT = RIGHT,DOWN = "\ue015",ARROW_DOWN = DOWN,INSERT = "\ue016",DELETE = "\ue017",SEMICOLON = "\ue018",EQUALS = "\ue019",NUMPAD0 = "\ue01a" # number pad keys,NUMPAD1 = "\ue01b",NUMPAD2 = "\ue01c",NUMPAD3 = "\ue01d",NUMPAD4 = "\ue01e",NUMPAD5 = "\ue01f",NUMPAD6 = "\ue020",NUMPAD7 = "\ue021",NUMPAD8 = "\ue022",NUMPAD9 = "\ue023",MULTIPLY = "\ue024",ADD = "\ue025",SEPARATOR = "\ue026",SUBTRACT = "\ue027",DECIMAL = "\ue028",DIVIDE = "\ue029",,F1 = "\ue031" # function keys,F2 = "\ue032",F3 = "\ue033",F4 = "\ue034",F5 = "\ue035",F6 = "\ue036",F7 = "\ue037",F8 = "\ue038",F9 = "\ue039",F10 = "\ue03a",F11 = "\ue03b",F12 = "\ue03c",,META = "\ue03d",COMMAND = "\ue03d",ZENKAKU_HANKAKU = "\ue040"
            # https: // github.com / SeleniumHQ / selenium / blob / trunk / py / selenium / webdriver / common / keys.py

    def execute_keyboard_with_element(self, driver, key_board, element_page, device):
        try:
            element = self.get_element_by_from_device(element_page, device, driver)
            attribute, value, list_key = self.get_value_key_code(key_board)
            element.send_keys(value)
            # action.send_keys(Keys)
        except NoSuchElementException:
            print(f"Element with locator '{element_page}' not found")
        except Exception as e:
            print(f"An error occurred while executing keyboard with element: {str(e)}")

    def execute_keyboard_without_element(self, driver, key_board, key_action, device):
        try:
            action = ActionChains(driver)
            attribute, value, list_key = self.get_value_key_code(key_action)
            attribute = self.change_keyboard_with_mac_env(attribute)
            if key_board == 'KEY_DOWN':
                if list_key[1]:
                    action.key_down(Keys().__getattribute__(attribute)).send_keys(list_key[1])
                else:
                    action.key_down(Keys().__getattribute__(attribute))
            elif key_board == 'KEY_UP':
                if list_key[1]:
                    action.key_up(Keys().__getattribute__(attribute)).send_keys(list_key[1])
                else:
                    action.key_up(Keys().__getattribute__(attribute))
            action.perform()
            sleep(int(0.5))
            # action.send_keys(Keys)
        except Exception as e:
            logger.error(f"An error occurred while executing keyboard with element: {str(e)}")
            assert False, f'An error occurred while executing action with keyboard {key_action}'

    def get_value_key_code(self, key_name):
        try:
            list_key = key_name.split('+')
            for attribute, value in Keys.__dict__.items():
                if list_key[0].replace("'", "") == attribute:
                    return attribute, value, list_key
        except Exception as e:
            print('An error occurred while getting key code:', key_name)
            return None, None, None

    def change_keyboard_with_mac_env(self, attribute):
        """
        Change the keyboard attribute based on the macOS environment.

        Args:
            attribute (str): The original keyboard attribute.

        Returns:
            str: The updated keyboard attribute.
        """
        import platform
        # Get the current operating system
        os = platform.platform()
        # Check if the OS is macOS and if the attribute is 'CONTROL'
        if os.__contains__('macOS') and attribute == 'CONTROL':
            return 'COMMAND'
        else:
            return attribute

    def execute_javascript_with_element(self, root_path, element_page, javascript_file, driver, device):
        from Utilities.read_configuration import read_configuration
        logger.info(f"perform with action javascript {javascript_file}")
        try:
            element = self.get_element_by_from_device(element_page, device, driver)
            data = read_configuration().get_content_javascript(root_path, javascript_file)
            result = driver.execute_script(data, element)
            if isinstance(result, bool):
                assert result, f"failed when execute javascript file {javascript_file}"
        except NoSuchElementException:
            logger.error(f"Element with locator '{element_page}' not found")
            assert False, f"Element with locator '{element_page}' not found"
        except Exception as e:
            logger.error(f"An error occurred while executing JavaScript with element: {str(e)}")
            assert False, f"An error occurred while executing JavaScript with element: {str(e)}"

    def execute_javascript_without_element(self, root_path, javascript_file, driver, device):
        from Utilities.read_configuration import read_configuration
        logger.info(f"perform with action javascript {javascript_file}")
        try:
            data = read_configuration().get_content_javascript(root_path, javascript_file)
            result = driver.execute_script(data)
            if isinstance(result, bool):
                assert result, f"fail when execute javascript file {javascript_file}"
        except Exception as e:
            logger.error(f"fail when execute javascript file {javascript_file}")
            assert False, f"fail when execute javascript file {javascript_file}"

    def execute_javascript_with_table(self, root_path, arr_element_page, javascript_file, driver, device):
        from Utilities.read_configuration import read_configuration
        logger.info(f"perform with action javascript {javascript_file}")
        data = read_configuration().get_content_javascript(root_path, javascript_file)
        try:
            args = []
            for element in arr_element_page:
                args.append(self.get_element_by_from_device(element, device, driver))
            result = driver.execute_script(data, *args)
            if isinstance(result, bool):
                assert result, f"fail when execute javascript file {javascript_file}"
        except Exception as e:
            logger.error(f"fail when execute javascript file {javascript_file}")
            assert False, f"fail when execute javascript file {javascript_file}"

    def handle_element_not_interactable_exception(self, element_page, action, driver, value, wait, dict_save_value, device, context, count_number=0):
        logger.debug(f'handle element not interactable exception {element_page}')
        element = self.get_element_by_from_device(element_page, device, driver)
        try:
            if device['platformName'] == "WEB":
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", element)
        except Exception as e:
            assert True, f"fail when scroll to element {element}, skip step scroll to element"
        while count_number < 10:
            sleep(1)
            count_number += 1
            logger.debug(f'count number {count_number}')
            self.action_page(element_page, action, driver, value, wait, dict_save_value, device, context, count_number)
            break

    def handle_invalid_element_state_exception(self, value, element_page, device, driver, action):
        element = self.get_element_by_from_device(element_page, device, driver)
        action_chains = ActionChains(driver)
        try:
            if device['platformName'] == "WEB":
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", element)
        except Exception as e:
            assert True, f"fail when scroll to element {element}, skip step scroll to element"
        match action:
            case "click":
                action_chains.click(element)
                action_chains.perform()
            case "type":
                action_chains.send_keys(value)
                action_chains.perform()
            case "text":
                action_chains.send_keys(value)
                action_chains.perform()
            case _:
                logger.error(f"not exist {action} in element not interactable exception")
                assert False, f"not exist {action} in element not interactable exception"

    def execute_action(self, page, action_id, driver, wait, table, dict_save_value, platform_name, context, is_loop):
        """
           Executes a specified action on a web page.

           Args:
               page (dict): The page object containing the actions.
               action_id (str): The ID of the action to execute.
               driver (WebDriver): The web driver instance.
               wait (WebDriverWait): The web driver wait instance.
               table (list): The table data.
               dict_save_value (dict): The dictionary containing saved values.
               platform_name (str): The name of the platform.
               context: The context of the action.
               is_loop: Flag indicating if action is part of a loop.

           Returns:
               bool: Indicates if the loop should break.

           Raises:
               AssertionError: If the action or element cannot be executed.
               FileNotFoundError: If the page file is not found.
               YAMLError: If there is an error reading the YAML file.
           """
        dict_action = page['actions']
        dict_action = list(filter(
            lambda action: action['id'] == action_id, dict_action
        ))
        type_action = None
        result = True
        is_break = False
        if dict_action:
            obj_action = dict_action[0]
            arr_list_action = obj_action['actionElements']
            for index, action_elements in enumerate(arr_list_action):
                value = ""
                if table:
                    for row in table:
                        if action_elements['element']['id'] == row["Field"]:
                            value = row["Value"]
                            result = False
                            break
                    if result:
                        if self.check_field_exist(action_elements, "inputType"):
                            value = action_elements['inputType']
                            result = False
                else:
                    if self.check_field_exist(action_elements, "inputType"):
                        value = action_elements['inputType']
                        value = procees_value().get_value(value, dict_save_value)

                element_page = action_elements['element']
                locator = ManagementFile().get_locator_from_action(element_page, platform_name)
                if self.check_field_exist(action_elements, "condition") and self.check_field_exist(
                        action_elements, "timeout"):
                    try:
                        result = self.wait_element_for_status(locator, action_elements['condition'], driver,
                                                              platform_name, action_elements['timeout'], True)
                        if self.check_field_exist(action_elements, 'inputType') and result == "PASS":
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text", "scroll"]:
                                self.action_page(locator, type_action, driver, value, action_elements['timeout'],
                                                 dict_save_value, platform_name, context, count_number=0)
                            else:
                                self.action_page(locator, "text", driver, type_action, action_elements['timeout'],
                                                 dict_save_value, platform_name, context, count_number=0)
                        is_break = self.check_status_to_break_loop(is_loop, index, arr_list_action, result)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action, locator['value'])
                        assert False, "can not execute action with element have value" + locator + "in framework"
                elif self.check_field_exist(action_elements, 'condition') and self.check_field_exist(action_elements,
                                                                                                     'timeout') is False:
                    try:
                        result = self.wait_element_for_status(locator, action_elements['condition'], driver, platform_name, wait,
                                                     False)
                        if self.check_field_exist(action_elements, 'inputType'):
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text", "scroll"]:
                                self.action_page(locator, type_action, driver, value, wait, dict_save_value,
                                                 platform_name, context, count_number=0)
                            else:
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value, platform_name,
                                                 context, count_number=0)
                        else:
                            self.wait_element_for_status(locator, action_elements['condition'], driver, platform_name,
                                                         wait, False)
                        is_break = self.check_status_to_break_loop(is_loop, index, arr_list_action, result)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator['value'])
                        assert False, "can not execute action " + type_action + " with element have value" + locator[
                            'value'] + "in framework"
                else:
                    try:
                        if self.check_field_exist(action_elements, 'inputType'):
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text", "scroll"]:
                                self.action_page(locator, type_action, driver, value, wait, dict_save_value,
                                                 platform_name, context, count_number=0)
                            else:
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value, platform_name,
                                                 context, count_number=0)
                            is_break = self.check_status_to_break_loop(is_loop, index, arr_list_action)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator.value)
                        assert False, "can not execute action " + type_action + " with element have value" + locator.value + "in framework"
            return is_break
        else:
            logger.error(f'Not Found Action {action_id} in page yaml')
            assert False, "Not Found Action " + action_id + " in page yaml"

    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except Exception as e:
            logger.warning(f'{str(e)}, ignore this error as this field is not exist')
            return False
    def check_status_to_break_loop(self, is_loop, index, array, result):
        if index == len(array) - 1 and is_loop and result in ["PASS"]:
            return True
        return False



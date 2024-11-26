import logging
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from faker import Faker
from selenium.common import NoSuchElementException, NoSuchFrameException, NoSuchWindowException, \
    StaleElementReferenceException, ElementNotInteractableException, InvalidElementStateException, \
    ElementNotVisibleException, ElementClickInterceptedException, TimeoutException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Utilities.action_mobile import ManagementFileAndroid
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

    def __init__(self):
        self.ACTION_CLICK = "click"
        self.ACTION_DOUBLE_CLICK = "double-click"
        self.ACTION_RIGHT_CLICK = "right-click"
        self.ACTION_SELECT = "select"
        self.ACTION_TYPE = "type"
        self.ACTION_TEXT = "text"
        self.ACTION_CLEAR = "clear"
        self.ACTION_HOVER_OVER = "hover-over"
        self.ACTION_SCROLL = "scroll"

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def action_page(
            self, element_page, action, driver, value, wait, dict_save_value, device, context, count_number=0
    ):
        """
        Executes a specified action on a web element.

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
            # Locate the element
            element = self.get_element_by_from_device(element_page, device, driver)
            logger.info(f"Performing '{action}' on element with locator: {element_page.get('value')}")

            # Highlight the element if enabled in the context
            if getattr(context, "highlight", False):
                self.highlight(element, 0.3, context.highlight)

            # Process the value if needed
            if value:
                value = procees_value().get_value(value, dict_save_value)
                value = get_test_data_for(value, dict_save_value)

            # Ensure ACTIONS_MAP is initialized
            if not hasattr(self, "ACTIONS_MAP"):
                self._initialize_actions_map()

            # Check if the action is supported and execute it
            if action in self.ACTIONS_MAP:
                action_function = self.ACTIONS_MAP[action]
                self._execute_action(action_function, action, element, driver, wait, value, device, element_page)
                logger.info(f"Action '{action}' successfully performed.")
            else:
                logger.error(f"Unsupported action: {action}")
                raise AssertionError(f"Action '{action}' is not supported by the framework.")
        except (ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException) as e:
            logger.warning(f"Retrying due to known interaction issue ({type(e).__name__}): {str(e)}")
            self.handle_element_not_interactable_exception(
                element_page, action, driver, value, wait, dict_save_value, device, context, count_number
            )
        except InvalidElementStateException as e:
            logger.error(f"Invalid state for element during action '{action}': {str(e)}")
            self.handle_invalid_element_state_exception(value, element_page, device, driver, action)
        except Exception as e:
            logger.error(f"Unexpected error performing '{action}' on element: {str(e)}")
            raise

    def _initialize_actions_map(self):
        """Initializes the ACTIONS_MAP with supported actions."""
        self.ACTIONS_MAP = {
            self.ACTION_CLICK: self._handle_click_action,
            self.ACTION_DOUBLE_CLICK: self._handle_double_click_action,
            self.ACTION_RIGHT_CLICK: self._handle_right_click_action,
            self.ACTION_SELECT: self._handle_select_action,
            self.ACTION_TYPE: self._handle_type_action,
            self.ACTION_TEXT: self._handle_type_action,  # Alias for "type"
            self.ACTION_CLEAR: self._handle_clear_action,
            self.ACTION_HOVER_OVER: self._handle_hover_over_action,
            self.ACTION_SCROLL: self._handle_scroll_action,
        }
        # self.ACTIONS_MAP = {
        #     "click": lambda element, wait, element_page, device, driver: self.click_action(
        #         element, wait, element_page, device, driver
        #     ),
        #     "double-click": lambda element, driver: ActionChains(driver).double_click(element).perform(),
        #     "right-click": lambda element, driver: ActionChains(driver).context_click(element).perform(),
        #     "select": lambda element, value: Select(element).select_by_visible_text(value),
        #     "type": lambda element, value: element.send_keys(value),
        #     "text": lambda element, value: element.send_keys(value),
        #     "clear": lambda element: element.clear(),
        #     "hover-over": lambda element, driver, action, device: self.mouse_action(element, driver, action, device),
        #     "scroll": lambda element, driver, device: self.scroll_to_element(element, driver, False, device, False),
        # }

    def _handle_click_action(self, element, wait, element_page, device, driver):
        """Handles a click action."""
        self.click_action(element, wait, element_page, device, driver)

    def _handle_double_click_action(self, element, driver):
        """Handles a double-click action."""
        ActionChains(driver).double_click(element).perform()

    def _handle_right_click_action(self, element, driver):
        """Handles a right-click action."""
        ActionChains(driver).context_click(element).perform()

    def _handle_select_action(self, element, value):
        """Handles a select action (by visible text)."""
        Select(element).select_by_visible_text(value)

    def _handle_type_action(self, element, value):
        """Handles typing text into an element."""
        element.send_keys(value)

    def _handle_clear_action(self, element):
        """Handles clearing the text of an element."""
        element.clear()

    def _handle_hover_over_action(self, element, driver, action, device):
        """Handles hovering over an element."""
        self.mouse_action(element, driver, action, device)

    def _handle_scroll_action(self, element, driver, flag, device, is_highlight):
        """Handles scrolling to an element."""
        self.scroll_to_element(element, driver, flag, device, is_highlight)
    def _execute_action(self, action_function, action, element, driver, wait, value, device, element_page):
        """
        Executes the appropriate action based on the provided function and parameters.

        Args:
            action_function (callable): The function to execute for the action.
            action (str): The action being performed.
            element (WebElement): The target web element.
            driver (WebDriver): Selenium WebDriver instance.
            wait (WebDriverWait): Explicit wait object.
            value (str): Value to use for certain actions.
            device (str): Target device context.
            element_page (dict): Element details such as locator strategy and value.
        """
        if action in {"type", "text", "select"}:
            action_function(element, value)
        elif action in {"double-click", "right-click"}:
            action_function(element, driver)
        elif action == "hover-over":
            action_function(element, driver, action, device)
        elif action == "scroll":
            action_function(element, driver, False, device , False)
        elif action == "click":
            action_function(element, wait, element_page, device, driver)
        elif action == "clear":
            action_function(element)
        else:
            logger.error(f"Unhandled action: {action}")
            raise AssertionError(f"Action '{action}' is not implemented.")

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
            if not hasattr(self, "STATUS_CONDITIONS"):
                self._initialize_status_conditions()
            if status not in self.STATUS_CONDITIONS:
                raise ValueError(f"Unsupported status: {status}")

            condition = self.STATUS_CONDITIONS[status]
            # Status mapping for WebDriverWait conditions
            if status in ["EXISTED", "NOT_EXISTED"]:
                condition(element_page, driver, device, wait)
            else:
                condition(driver, wait, locator_from_wait)
            logger.info(f"Element '{element_page['value']}' successfully achieved status '{status}'")
            return "PASS"
        except Exception as e:
            # Log the error
            logger.error(f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}")
            # Handle test flow based on the `flag`
            assert flag, f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}"
            if flag:
                return "SKIP"

    def _initialize_status_conditions(self):
        # Define status conditions once as a class-level dictionary
        self.STATUS_CONDITIONS = {
            "DISPLAYED": lambda driver, wait, locator: self.wait_displayed(locator, driver, wait),
            "NOT_DISPLAYED": lambda driver, wait, locator: self.wait_not_displayed(locator, driver, wait),
            "ENABLED": lambda driver, wait, locator: self.wait_enabled(locator, driver, wait),
            "NOT_ENABLED": lambda driver, wait, locator: self.wait_not_enabled(locator, driver, wait),
            "EXISTED": lambda element_page, driver, device, wait: self.wait_existed(element_page, driver, device, wait),
            "NOT_EXISTED": lambda element_page, driver, device, wait: self.wait_not_existed(element_page, driver,
                                                                                            device, wait),
            "SELECTED": lambda driver, wait, locator: self.wait_selected(locator, driver, wait),
            "NOT_SELECTED": lambda driver, wait, locator: self.wait_not_selecte(locator, driver, wait),
        }

    def wait_displayed(self, locator, driver, wait):
        WebDriverWait(driver, wait).until(ec.visibility_of_element_located(locator))

    def wait_not_displayed(self, locator, driver, wait):
        WebDriverWait(driver, wait).until(ec.invisibility_of_element_located(locator))

    def wait_enabled(self, locator, driver, wait):
        WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator))

    def wait_not_enabled(self, locator, driver, wait):
        WebDriverWait(driver, wait).until_not(ec.element_to_be_clickable(locator))

    def wait_existed(self, element_page, driver, device, wait):
        WebDriverWait(driver, wait).until(
            lambda _: len(self.get_list_element_by_from_device(element_page, device, driver)) > 0)

    def wait_not_existed(self, element_page, driver, device, wait):
        WebDriverWait(driver, wait).until(
            lambda _: len(self.get_list_element_by_from_device(element_page, device, driver)) == 0)

    def wait_selected(self, locator, driver, wait):
        WebDriverWait(driver, wait).until(ec.element_located_to_be_selected(locator))

    def wait_not_selecte(self, locator, driver, wait):
        WebDriverWait(driver, wait).until_not(ec.element_located_to_be_selected(locator))

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
            # Apply regex if specified
            if is_regex:
                if not pattern:
                    raise ValueError("Regex pattern must be provided when is_regex is True.")
                match = re.search(pattern, value)
                if not match:
                    raise ValueError(f"Regex pattern '{pattern}' did not match any part of the value: '{value}'.")
                value = match.group(1)
                logger.debug(f"Value after regex extraction: '{value}'")
            # Save the value to the dictionary
            # Save the extracted value into the dictionary
            dict_save_value[f"KEY.{key}"] = value
            logger.info(f"Text saved successfully for key: 'KEY.{key}'")
            return dict_save_value
        except Exception as e:
            # Log the error if the wait fails
            logger.error(f"Failed to save text for element '{element_page['value']}' with key '{key}': {str(e)}")
            raise AssertionError(f"Failed to save text for element '{element_page['value']}' with key '{key}'") from e

    def get_locator_for_wait_from_device(self, element_page: dict) -> tuple:
        """
        Get the locator for waiting based on the device platform.

        Args:
            element_page (dict): The element page specification. Must include:
                - 'device': The device platform (e.g., 'WEB', 'ANDROID', 'IOS').
                - 'type': The locator type (e.g., 'id', 'xpath').
                - 'value': The locator value.

        Returns:
            tuple: The locator for waiting, e.g., (By.ID, "some-id").

        Raises:
            ValueError: If the device platform is unknown or unsupported.
        """
        # Validate input
        device_platform = element_page.get('device')
        if not device_platform:
            raise ValueError("Device platform is not specified in 'element_page'.")

        logger.info(f"Fetching locator for device platform: {device_platform}")

        # Map device platform to the corresponding management file
        try:
            if device_platform == "WEB":
                locator = ManagementFile().get_locator_for_wait(element_page['type'], element_page['value'])
            elif device_platform in {"ANDROID", "IOS"}:
                locator = ManagementFileAndroid().get_locator_for_wait(element_page['type'], element_page['value'])
            else:
                raise ValueError(f"Unsupported device platform: {device_platform}")

            logger.debug(f"Locator obtained: {locator}")
            return locator

        except Exception as e:
            logger.error(f"Failed to get locator for platform '{device_platform}': {str(e)}")
            raise

    def get_list_element_by_from_device(
            self,
            element_page: dict,
            device: dict,
            driver
    ) -> list:
        """
        Get a list of elements based on the device platform.

        Args:
            element_page (dict): The element page specification, including:
                - 'type': The locator type (e.g., 'id', 'xpath').
                - 'value': The locator value.
            device (dict): The device information, including 'platformName'.
            driver: The Selenium WebDriver instance.

        Returns:
            list: A list of WebElements found on the page.

        Raises:
            ValueError: If the device platform is unknown or unsupported.
        """
        platform_name = device.get('platformName')

        if not platform_name:
            raise ValueError("Device information is missing or 'platformName' is not specified.")

        logger.info(f"Fetching list of elements for platform: {platform_name}")

        try:
            if platform_name == "WEB":
                elements = ManagementFile().get_list_element_by(element_page['type'], driver, element_page['value'])
            elif platform_name in {"ANDROID", "IOS"}:
                elements = ManagementFileAndroid().get_list_element_by(element_page['type'], driver,
                                                                       element_page['value'])
            else:
                raise ValueError(f"Unsupported device platform: {platform_name}")

            logger.debug(f"Successfully fetched {len(elements)} elements for platform: {platform_name}")
            return elements

        except Exception as e:
            logger.error(f"Failed to fetch list of elements for platform '{platform_name}': {str(e)}")
            raise

    def get_element_by_from_device(
            self,
            element_page: dict,
            device: dict,
            driver
    ):
        """
        Get a single element based on the device platform.

        Args:
            element_page (dict): The element page specification, including:
                - 'device': The device platform (e.g., 'WEB', 'ANDROID', 'IOS').
                - 'type': The locator type (e.g., 'id', 'xpath').
                - 'value': The locator value.
            device (dict): The device information.
            driver: The Selenium WebDriver instance.

        Returns:
            WebElement: The found WebElement.

        Raises:
            ValueError: If the device platform is unknown or unsupported.
        """
        platform_name = element_page.get('device')

        if not platform_name:
            raise ValueError("Device platform is not specified in 'element_page'.")

        logger.info(f"Fetching element for platform: {platform_name}")

        try:
            if platform_name == "WEB":
                element = ManagementFile().get_element_by(element_page['type'], driver, element_page['value'])
            elif platform_name in {"ANDROID", "IOS"}:
                element = ManagementFileAndroid().get_by_mobile(element_page['type'], driver, element_page['value'])
            else:
                raise ValueError(f"Unsupported device platform: {platform_name}")

            logger.debug(f"Successfully fetched element for platform: {platform_name}")
            return element

        except Exception as e:
            logger.error(f"Failed to fetch element for platform '{platform_name}': {str(e)}")
            raise

    def get_value_element_form_device(
            self,
            element,
            device: dict,
            element_page: dict,
            driver
    ) -> str:
        """
        Retrieves the value of the element based on the device platform.

        Args:
            element: The WebElement to retrieve the value from.
            device (dict): The device platform information, including 'platformName'.
            element_page (dict): The element page specification.
            driver: The Selenium WebDriver instance.

        Returns:
            str: The value of the element based on the platform.

        Raises:
            Exception: If the element value cannot be retrieved.
        """
        try:
            platform_name = device.get('platformName')
            if not platform_name:
                raise ValueError("Device platform name ('platformName') is missing in the device information.")

            logger.info(f"Fetching value for element on platform: {platform_name}")

            if platform_name == "WEB":
                # Handle web elements specifically
                try:
                    if element.get_attribute("value") and element.tag_name.lower() == "input":
                        logger.info("Element is an input field. Fetching 'value' attribute.")
                        return element.get_attribute("value")

                    # Fallback to text content
                    text = element.text.strip()
                    if not text:
                        logger.debug("No visible text found. Trying 'innerText' attribute.")
                        text = element.get_attribute("innerText").strip()
                    if text:
                        logger.info(f"Text found on element: {text}")
                        return text

                    raise ValueError("Unable to retrieve value from the web element.")

                except (ElementNotInteractableException, StaleElementReferenceException) as e:
                    logger.warning(f"Element not interactable or stale: {e}. Retrying...")
                    sleep(2)
                    element = self.get_element_by_from_device(element_page, device, driver)
                    return self.get_value_element_form_device(element, device, element_page, driver)

            else:
                # Handle non-web elements (e.g., Android, iOS)
                logger.info("Fetching text content for non-web element.")
                return element.text.strip()

        except Exception as e:
            logger.error(f"Failed to fetch value for element: {str(e)}")
            raise

        finally:
            self.count_number = 0

    def get_value_attribute_element_form_device(
            self,
            element,
            device: dict,
            value: str,
            flag: bool
    ) -> str:
        """
        Retrieves the value of a specified attribute or CSS property from an element based on the platform.

        Args:
            element: The WebElement to retrieve the attribute value from.
            device (dict): The device platform information, including 'platformName'.
            value (str): The name of the attribute or CSS property to retrieve.
            flag (bool): Whether to retrieve the value using a CSS property (True) or an attribute (False).

        Returns:
            str: The value of the specified attribute or CSS property.

        Raises:
            ValueError: If the device platform is not supported or invalid arguments are provided.
        """
        try:
            platform_name = device.get('platformName')
            if not platform_name:
                raise ValueError("Device platform name ('platformName') is missing in the device information.")

            logger.info(f"Fetching attribute '{value}' for platform: {platform_name}")

            if platform_name == "WEB":
                if flag:
                    # Retrieve value using CSS property
                    value_attribute = element.value_of_css_property(value)
                    if 'color' in value:
                        hex_color = Color.from_string(value_attribute).hex.lower()
                        logger.debug(f"Retrieved color property: {hex_color}")
                        return hex_color
                    else:
                        result = value_attribute.lower()
                        logger.debug(f"Retrieved CSS property: {result}")
                        return result
                else:
                    # Retrieve value using attribute
                    attribute_value = element.get_attribute(value)
                    logger.debug(f"Retrieved attribute value: {attribute_value}")
                    return attribute_value

            elif platform_name in {"ANDROID", "IOS"}:
                # For mobile platforms, always retrieve the value using get_attribute
                attribute_value = element.get_attribute(value)
                logger.debug(f"Retrieved attribute value for mobile platform: {attribute_value}")
                return attribute_value

            else:
                raise ValueError(f"Unsupported device platform: {platform_name}")

        except Exception as e:
            logger.error(f"Failed to retrieve attribute '{value}' for platform '{platform_name}': {str(e)}")
            raise

    from faker import Faker
    import logging

    logger = logging.getLogger(__name__)

    def create_random_user(self, locale: str = "en_US") -> dict:
        """
        Generate a random user with fake data.

        Args:
            locale (str): The locale to use for generating the fake data. Defaults to 'en_US'.

        Returns:
            dict: A dictionary containing the generated user data.

        Raises:
            ValueError: If the provided locale is invalid or unsupported.
        """
        try:
            # Initialize Faker with the provided locale
            faker = Faker(locale)
            logger.info(f"Creating random user with locale: {locale}")

            # Generate user data
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

            # Log the generated user data
            logger.debug(f"Generated user data: {user}")
            return user

        except ValueError as ve:
            logger.error(f"Invalid locale provided: {locale}. Error: {str(ve)}")
            raise ValueError(f"Unsupported or invalid locale: {locale}") from ve

        except Exception as e:
            logger.error(f"An error occurred while creating random user: {str(e)}")
            raise RuntimeError("Failed to generate random user data.") from e

    def verify_elements_below_attributes(
            self,
            page: dict,
            row: list,
            platform_name: str,
            dict_save_value: dict,
            driver,
            device: dict,
            wait,
            is_highlight: bool,
            page_present: str
    ):
        """
        Verify the attributes and status of elements on a given page.

        Args:
            page (dict): The page specification containing elements to verify.
            row (list): The row containing the element attributes to verify.
                        Format: [element_id, value, status, helper].
            platform_name (str): The platform for which the elements are being verified.
            dict_save_value (dict): A dictionary of saved values for substitutions.
            driver: The Selenium WebDriver instance.
            device (dict): The device information.
            wait: The WebDriverWait instance.
            is_highlight (bool): Whether to highlight the element during verification.
            page_present (str): The current page name for logging and error messages.

        Raises:
            AssertionError: If the element is not found or if verification fails.
        """
        try:
            element_id, value, status, helper = row

            # Filter for the target element by ID
            arr_element = [el for el in page.get('elements', []) if el['id'] == element_id]
            if not arr_element:
                error_msg = f"Element with ID {element_id} not found in dictionary {page_present}"
                logger.error(error_msg)
                raise AssertionError(error_msg)

            logger.info(f"Verifying element '{element_id}' with value '{value}' and status '{status}'")

            # Process value using saved values if needed
            value = procees_value().get_value(value, dict_save_value) if value else ""

            # Fetch the element definition from YAML
            element_yaml = self.get_element(page, element_id, platform_name, dict_save_value)
            if not element_yaml:
                error_msg = f"Element with ID {element_id} and value '{value}' not found on the page."
                logger.error(error_msg)
                raise AssertionError(error_msg)

            # Verify status and value
            if status and element_yaml:
                self.wait_element_for_status(element_yaml, status, driver, device, wait, False)

                if value and not helper:
                    logger.info(f"Validating value '{value}' for element '{element_id}'")
                    self.verify_value_in_element(element_yaml, value, device, driver, is_highlight, wait)
                else:
                    logger.info(f"Element '{element_id}' status '{status}' validated without value check.")

            else:
                raise AssertionError("Both field name and status are required for validation.")

            # Verify with helpers if provided
            if helper:
                logger.info(f"Validating element '{element_id}' with helper '{helper}'")
                self.verify_value_with_helpers(value, helper, element_yaml, device, driver, is_highlight)

            logger.info(f"Verification completed for element '{element_id}'")

        except AssertionError as ae:
            logger.error(f"Assertion failed: {str(ae)}")
            raise

        except Exception as e:
            logger.error(f"An error occurred during verification: {str(e)}")
            raise RuntimeError(f"Error verifying elements on page '{page_present}': {str(e)}")

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

    def verify_value_in_element(self, element_page, expected_value, device, driver, is_highlight, wait):
        """
        Verifies that the value of an element matches the expected value.

        Args:
            element_page (dict): Element locator details (type and value).
            expected_value (str): The expected value to compare against.
            device (dict): Device information (e.g., platform details).
            driver (WebDriver): The Selenium WebDriver instance.
            is_highlight (bool): Whether to highlight the element for debugging.
            wait (int): Maximum wait time in seconds.

        Raises:
            AssertionError: If the element is not found or the value does not match the expected value.
        """
        element_name = element_page.get("value", "unknown")
        try:
            # Get the locator for waiting and wait until the element is present
            locator = common_device().get_locator_for_wait_from_device(element_page)
            logger.info(f"Waiting for element '{element_name}' to be present.")
            WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator))

            # Find the element
            element = self.get_element_by_from_device(element_page, device, driver)

            # Scroll to the element and optionally highlight it
            if device['platformName'].upper() == "WEB":
                self.scroll_to_element_by_js(element, driver, True, device['platformName'], is_highlight)

            # Get the value of the element
            actual_value = self.get_value_element_form_device(element, device, element_page, driver)
            logger.debug(f"Actual value of the element: '{actual_value}'")
            logger.debug(f"Expected value: '{expected_value}'")

            # Verify the actual value matches the expected value
            assert actual_value == expected_value, (
                f"Value mismatch: Actual value is '{actual_value}', "
                f"but expected '{expected_value}'."
            )
            logger.info(f"Value verification for element '{element_name}' passed.")
        except TimeoutException:
            logger.error(f"Timeout: Element '{element_name}' was not found within {wait} seconds.")
            raise AssertionError(f"Timeout: Element '{element_name}' not found within {wait} seconds.")
        except NoSuchElementException:
            logger.error(f"Element '{element_name}' not found.")
            raise AssertionError(f"Element '{element_name}' not found.")
        except Exception as e:
            logger.error(f"Unexpected error verifying value for element '{element_name}': {str(e)}")
            raise AssertionError(f"Unexpected error verifying value for element '{element_name}'.") from e

    def verify_value_with_helpers(self, expected, helper, element_page, device, driver, is_highlight):
        """
        Verifies an element's value or attribute using helper conditions.

        Args:
            expected (str): The expected value or pattern.
            helper (str): The helper condition to validate (e.g., 'CONTAINS', 'COLOR').
            element_page (dict): Element locator details.
            device (dict): Device information (e.g., platform details).
            driver (WebDriver): The Selenium WebDriver instance.
            is_highlight (bool): Whether to highlight the element for debugging.

        Raises:
            AssertionError: If the validation fails.
        """
        unsupported_helpers = [
            'BACKGROUND-COLOR', 'COLOR', 'FONT_FAMILY', 'FONT_SIZE',
            'FONT_WEIGHT', 'FONT_HEIGHT', 'TEXT_ALIGN'
        ]

        if helper in unsupported_helpers and device['platformName'] != 'WEB':
            raise AssertionError(f"Framework only supports '{helper}' for WEB environments, not native apps.")

        if not helper or expected == '':
            logger.error("The helper and expected value must both be provided.")
            raise AssertionError(f"Both helper and expected value are required. Helper: {helper}, Expected: {expected}")

        # Retrieve the element
        element = self.get_element_by_from_device(element_page, device, driver)
        self.scroll_to_element_by_js(element, driver, True, device['platformName'], is_highlight)

        # Retrieve element value or attribute based on the helper
        if helper in ["REGEX", "STARTS_WITH", "ENDS_WITH", "CONTAINS"]:
            value_element = self.get_value_element_form_device(element, device, element_page, driver)

            if helper == "REGEX":
                check_match_pattern(expected, value_element, "Value of element does not match the expected pattern.")
            elif helper == "STARTS_WITH":
                assert value_element.startswith(expected), (
                    f"Value '{value_element}' does not start with '{expected}'."
                )
            elif helper == "ENDS_WITH":
                assert value_element.endswith(expected), (
                    f"Value '{value_element}' does not end with '{expected}'."
                )
            elif helper == "CONTAINS":
                assert expected in value_element, (
                    f"Value '{value_element}' does not contain '{expected}'."
                )
        else:
            attribute_name = helper.lower().replace("_", "-")  # Map helper to CSS-like attribute name
            is_css_property = helper in unsupported_helpers
            value_attribute = self.get_value_attribute_element_form_device(
                element, device, attribute_name, is_css_property
            )

            assert value_attribute == expected.lower(), (
                f"'{attribute_name}' of element is '{value_attribute}', but expected '{expected}'."
            )

        logger.info(f"Validation using helper '{helper}' for element '{element_page.get('value', 'unknown')}' passed.")

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
        if is_hightlight:
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
        """
        Performs a mouse or touch action on an element based on the device and action type.

        Args:
            element: The target element for the action.
            driver: The WebDriver or Appium Driver instance.
            action: The type of action to perform (e.g., 'hover-over').
            device: A dictionary containing device information, including 'platformName'.

        Returns:
            None
        """
        try:
            # Validate device type
            platform_name = device.get('platformName', '').upper()
            if platform_name not in ['WEB', 'MOBILE']:
                raise ValueError(f"Unsupported platformName: {platform_name}")

            # Perform the appropriate action based on device type
            if action == 'hover-over':
                if platform_name == 'WEB':
                    ActionChains(driver).move_to_element(element).perform()
                elif platform_name in ["ANDROID", "IOS"]:
                    TouchAction(driver).press(element).release().perform()
                else:
                    raise ValueError(f"Unsupported platformName: {platform_name}")
            else:
                raise ValueError(f"Unsupported action: {action}")

        except Exception as e:
            logging.error(f"Error performing mouse action '{action}' on {platform_name}: {e}", exc_info=True)

    def scroll_to_element_by_js(self, element, driver, flag=True, platform="WEB", is_highlight=False):
        """
        Scrolls to the specified Selenium WebDriver element using JavaScript.

        Args:
            element: The Selenium WebDriver element to scroll to.
            driver: The WebDriver instance.
            flag: A flag indicating whether to raise an error if scrolling fails. Defaults to True.
            platform: The platform name, only "WEB" is supported. Defaults to "WEB".
            is_highlight: Flag to determine if highlighting should be applied. Defaults to False.

        Returns:
            None

        Raises:
            AssertionError: If scrolling fails or if the platform is unsupported.
        """
        try:
            # Validate platform
            if platform.upper() == "WEB":

                # Execute JavaScript to scroll to the element
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", element
                )

                # Optionally highlight the element after scrolling
                if is_highlight:
                    self.highlight(element, 0.3, is_highlight)

                logging.info(f"Successfully scrolled to the element: {element}")
            else:
                logger.info(f"Scroll to element is only supported for the WEB platform. Provided: {platform}")
        except Exception as e:
            logging.error(f"Failed to scroll to the element: {element}. Error: {e}", exc_info=True)
            if flag:
                raise AssertionError(f"Failed to scroll to element: {element}") from e

    def scroll_to_element(self, element, driver, flag=True, platform="WEB", is_highlight=False):
        """
        Scrolls to the specified element on the webpage using Selenium or JavaScript.

        Args:
            element: The Selenium WebDriver element to scroll to.
            driver: The WebDriver instance.
            flag: A flag indicating whether to raise an error if scrolling fails. Defaults to True.
            platform: The platform name, only 'WEB' is supported. Defaults to 'WEB'.
            is_highlight: Flag to enable highlighting after scrolling. Defaults to False.

        Returns:
            None

        Raises:
            AssertionError: If scrolling fails and the flag is set to True.
        """
        if platform.upper() != "WEB":
            raise AssertionError(f"Scroll to element is only supported for the WEB platform. Provided: {platform}")

        try:
            # Try scrolling to the element using ActionChains
            logging.info(f"Attempting to scroll to element using ActionChains: {element}")
            ActionChains(driver).scroll_to_element(element).perform()

            # Optionally highlight the element
            if is_highlight:
                self.highlight(element, 0.3, is_highlight)

        except Exception as e:
            logging.warning(
                f"ActionChains scroll failed for element {element}. Attempting JavaScript scroll. Error: {e}")

            # Fallback to JavaScript scrolling
            try:
                self.scroll_to_element_by_js(element, driver, flag, platform, is_highlight)
            except Exception as js_e:
                logging.error(f"JavaScript scroll also failed for element {element}. Error: {js_e}")
                assert flag, f"Failed to scroll to element: {element}"


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
        """
        Switches to a frame by its index.

        Args:
            driver: The WebDriver instance.
            index: The index of the frame to switch to.

        Returns:
            None
        """
        try:
            # Ensure index is an integer
            index = int(index)

            # Attempt to switch to the frame using the index
            driver.switch_to.frame(index)
            logging.info(f"Successfully switched to frame with index {index}")

        except ValueError as e:
            # Handle the case where the index is not a valid integer
            self._handle_error(f"Index value must be an integer, got {type(index)}: {index}", e)

        except NoSuchFrameException as e:
            # Handle the case where the frame with the given index is not found
            self._handle_error(f"Frame with index {index} not found.", e)

        except WebDriverException as e:
            # Handle other WebDriver related exceptions
            self._handle_error(f"Failed to switch to frame with index {index}.", e)

        except Exception as e:
            # Catch any other unexpected exceptions
            self._handle_error(f"Unexpected error occurred while switching to frame with index {index}.", e)

    def _handle_error(self, message, exception):
        """
        Logs an error and raises a RuntimeError with the provided message and exception.

        Args:
            message: The error message to log and raise.
            exception: The exception to log and raise.

        Raises:
            RuntimeError: Always raises a RuntimeError with the given message.
        """
        logging.error(f"{message} Error: {exception}", exc_info=True)
        raise RuntimeError(message) from exception

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

    def handle_element_not_interactable_exception(self, element_page, action, driver, value, wait, dict_save_value,
                                                  device, context, count_number=0):
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
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator['value'])
                        assert False, "can not execute action with element have value" + locator + "in framework"
                elif self.check_field_exist(action_elements, 'condition') and self.check_field_exist(action_elements,
                                                                                                     'timeout') is False:
                    try:
                        result = self.wait_element_for_status(locator, action_elements['condition'], driver,
                                                              platform_name, wait,
                                                              False)
                        if self.check_field_exist(action_elements, 'inputType'):
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text", "scroll"]:
                                self.action_page(locator, type_action, driver, value, wait, dict_save_value,
                                                 platform_name, context, count_number=0)
                            else:
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value,
                                                 platform_name,
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
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value,
                                                 platform_name,
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

    def check_field_exist(self, dictionary, key):
        """
        Checks if a specific key exists in a dictionary and has a non-empty value.

        Args:
            dictionary (dict): The dictionary to check.
            key (str): The key to look for in the dictionary.

        Returns:
            bool: True if the key exists and has a value, False otherwise.

        Logs:
            A warning if the key does not exist or if accessing it raises an exception.
        """
        try:
            # Check if the key exists and has a non-empty value
            return bool(dictionary.get(key))
        except Exception as e:
            logger.warning(f"Error checking field '{key}': {str(e)}. This field does not exist or caused an error.")
            return False

    def check_status_to_break_loop(self, is_loop, index, array, result):
        if index == len(array) - 1 and is_loop and result in ["PASS"]:
            return True
        return False

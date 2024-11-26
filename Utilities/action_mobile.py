from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from project_runner import logger


class ManagementFileAndroid:
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.common.exceptions import NoSuchElementException
    locator_mapping = {
        "ID": AppiumBy.ID,
        "NAME": AppiumBy.NAME,
        "XPATH": AppiumBy.XPATH,
        "LINK TEXT": AppiumBy.LINK_TEXT,
        "PARTIAL LINK TEXT": AppiumBy.PARTIAL_LINK_TEXT,
        "CLASS NAME": AppiumBy.CLASS_NAME,
        "CSS": AppiumBy.CSS_SELECTOR,
        "ACCESSIBILITY_ID": AppiumBy.ACCESSIBILITY_ID,
        "PREDICATE": AppiumBy.IOS_PREDICATE,
        "CLASS_CHAIN": AppiumBy.IOS_CLASS_CHAIN,
    }

    def get_by_mobile(self, type_element, driver, value):
        """
        Retrieve a mobile element based on the specified locator type and value.

        :param type_element: The type of locator (e.g., ID, NAME, XPATH).
        :param driver: The WebDriver instance.
        :param value: The locator value.
        :return: The located element.
        :raises: Exception if the locator type is unsupported or element is not found.
        """
        logger.info(f"Attempting to locate element by '{type_element}' with value: '{value}'")

        # Define a mapping between type_element and AppiumBy locators
        # locator_mapping = {
        #     "ID": AppiumBy.ID,
        #     "NAME": AppiumBy.NAME,
        #     "XPATH": AppiumBy.XPATH,
        #     "LINK TEXT": AppiumBy.LINK_TEXT,
        #     "PARTIAL LINK TEXT": AppiumBy.PARTIAL_LINK_TEXT,
        #     "CLASS NAME": AppiumBy.CLASS_NAME,
        #     "CSS": AppiumBy.CSS_SELECTOR,
        #     "ACCESSIBILITY_ID": AppiumBy.ACCESSIBILITY_ID,
        #     "PREDICATE": AppiumBy.IOS_PREDICATE,
        #     "CLASS_CHAIN": AppiumBy.IOS_CLASS_CHAIN,
        # }

        # Ensure value for CLASS_CHAIN does not start with a slash
        if type_element == "CLASS_CHAIN" and value.startswith("/"):
            logger.debug("CLASS_CHAIN value starts with '/', removing it.")
            value = value[1:]

        # Get the Appium locator type
        appium_locator = self.locator_mapping.get(type_element)

        if not appium_locator:
            logger.error(f"Unsupported locator type: '{type_element}'.")
            raise Exception(f"Unsupported locator type: '{type_element}'")

        try:
            # Locate the element
            element = driver.find_element(appium_locator, value)
            logger.info(f"Successfully located element by '{type_element}' with value: '{value}'")
            return element

        except NoSuchElementException as e:
            logger.error(f"Element not found using '{type_element}' with value: '{value}'. Exception: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while locating element by '{type_element}' with value: '{value}'. Exception: {str(e)}")
            raise

    def get_list_element_by(self, type_element, driver, value):
        """
        Retrieve a list of mobile elements based on the specified locator type and value.

        :param type_element: The type of locator (e.g., ID, NAME, XPATH).
        :param driver: The WebDriver instance.
        :param value: The locator value.
        :return: A list of located elements.
        :raises: Exception if the locator type is unsupported or no elements are found.
        """
        logger.info(f"Attempting to locate elements by '{type_element}' with value: '{value}'")


        # Ensure value for CLASS_CHAIN does not start with a slash
        if type_element == "CLASS_CHAIN" and value.startswith("/"):
            logger.debug("CLASS_CHAIN value starts with '/', removing it.")
            value = value[1:]

        # Get the Appium locator type
        appium_locator = self.locator_mapping.get(type_element)

        if not appium_locator:
            logger.error(f"Unsupported locator type: '{type_element}'.")
            raise Exception(f"Unsupported locator type: '{type_element}'")

        try:
            # Locate the elements
            elements = driver.find_elements(appium_locator, value)

            if not elements:
                logger.warning(f"No elements found using '{type_element}' with value: '{value}'")
            else:
                logger.info(
                    f"Successfully located {len(elements)} element(s) by '{type_element}' with value: '{value}'")

            return elements

        except NoSuchElementException as e:
            logger.error(f"Elements not found using '{type_element}' with value: '{value}'. Exception: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while locating elements by '{type_element}' with value: '{value}'. Exception: {str(e)}")
            raise

    def get_locator(self, element_page, device):
        """
        Retrieve the locator for a specific device from an element page.

        :param element_page: The page object containing locators.
        :param device: The target device (e.g., WEB, ANDROID, IOS).
        :return: The matching locator object.
        :raises: Exception if no matching locator is found.
        """
        try:
            # Get the list of locators from the element page
            arr_locator = element_page.get_list_locator()

            # Iterate through locators to find a match for the device
            for locator in arr_locator:
                if locator.get_device() == device:
                    logger.info(f"Locator found for device: '{device}'")
                    return locator

            # If no matching locator is found, log an error and raise an exception
            logger.error(
                f"No locator found for device: '{device}'. Ensure the element_page contains the correct locators.")
            raise Exception(f"No locator found for device: '{device}'")

        except AttributeError as e:
            logger.error(f"AttributeError: {str(e)} - Ensure 'element_page' and its locators are properly defined.")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while retrieving locator for device: '{device}'. Exception: {str(e)}")
            raise

    def get_locator_from_action(self, element_page, device):
        """
        Retrieve a locator for a specific device from the element page's action data.

        :param element_page: A dictionary containing locators (e.g., {'locators': [...]})
        :param device: The target device (e.g., 'WEB', 'ANDROID', 'IOS').
        :return: The matching locator dictionary.
        :raises: Exception if no matching locator is found or if input data is malformed.
        """
        try:
            # Validate element_page structure
            if 'locators' not in element_page or not isinstance(element_page['locators'], list):
                logger.error(
                    "Invalid 'element_page' structure. Expected a dictionary with a 'locators' key containing a list.")
                raise ValueError(
                    "Invalid 'element_page' structure. Ensure it contains a 'locators' key with a list of locators.")

            # Iterate through locators to find the one matching the device
            for locator in element_page['locators']:
                if locator.get('device') == device:
                    logger.info(f"Locator found for device: '{device}'")
                    return locator

            # Log and raise error if no matching locator is found
            logger.error(f"No locator found for device: '{device}'. Check the locators in 'element_page'.")
            raise Exception(f"No locator found for device: '{device}'")

        except KeyError as e:
            logger.error(
                f"KeyError: {str(e)} - Ensure each locator in 'element_page['locators']' has the required keys.")
            raise
        except TypeError as e:
            logger.error(f"TypeError: {str(e)} - Ensure 'element_page' is a dictionary and 'locators' is a list.")
            raise
        except Exception as e:
            logger.error(
                f"An unexpected error occurred while retrieving locator for device: '{device}'. Exception: {str(e)}")
            raise

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def get_locator_for_wait(self, type, value):
        """
        Retrieve a locator tuple for waiting, based on the specified type and value.

        :param type: The locator type (e.g., 'ID', 'XPATH', 'CSS').
        :param value: The locator value.
        :return: A tuple containing the AppiumBy strategy and value.
        :raises: Exception if the locator type is unsupported.
        """
        try:
            logger.info(f"Getting locator for wait with type: '{type}' and value: '{value}'")

            # Handle CLASS_CHAIN value adjustments
            if type == "CLASS_CHAIN" and value.startswith("/"):
                logger.debug("CLASS_CHAIN value starts with '/', removing it.")
                value = value[1:]

            # Retrieve the corresponding AppiumBy locator
            appium_locator = self.locator_mapping.get(type)

            if not appium_locator:
                logger.error(f"Unsupported locator type: '{type}'")
                raise Exception(f"Unsupported locator type: '{type}'")

            locator = (appium_locator, value)
            logger.info(f"Successfully created locator: {locator}")
            return locator

        except Exception as e:
            logger.error(
                f"An error occurred while getting locator for type: '{type}', value: '{value}'. Exception: {str(e)}")
            raise

    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except:
            return False

    def action_mouse_mobile(self, action, element_page_from, element_page_to, context):
        """
        Perform a mobile touch action (e.g., drag-and-drop) between two elements.

        :param action: The action to perform (e.g., 'drag-and-drop').
        :param element_page_from: Dictionary containing type and value of the source element.
        :param element_page_to: Dictionary containing type and value of the target element.
        :param context: The context object containing the Appium driver.
        :raises: AssertionError if the action is not supported.
        """
        try:
            # Retrieve the source element
            element_from = self.get_by_mobile(element_page_from['type'], context.driver, element_page_from['value'])
            logger.info(f"Executing '{action}' with source element: {element_page_from['value']}")

            if action == 'drag-and-drop':
                # Retrieve the target element
                element_to = self.get_by_mobile(element_page_to['type'], context.driver, element_page_to['value'])

                # Perform the drag-and-drop action
                touch_action = TouchAction(context.driver)
                touch_action.long_press(element_from).move_to(element_to).release().perform()

                logger.info(f"Successfully executed '{action}' to target element: {element_page_to['value']}")
            else:
                # Handle unsupported actions
                logger.error(f"Unsupported action: '{action}'. Supported actions: ['drag-and-drop']")
                raise AssertionError(f"Unsupported action: '{action}'")

        except KeyError as e:
            logger.error(
                f"KeyError: Missing key in element_page: {str(e)}. Ensure both elements have 'type' and 'value'.")
            raise
        except Exception as e:
            logger.error(f"An error occurred while performing '{action}' between elements. Exception: {str(e)}")
            raise

    # def scroll_from_to_element(self, element_page_from, element_page_to, driver, wait):
    #     element_from_wait = self.get_locator_for_wait(element_page_from['type'], element_page_from['value'])
    #     element_to_wait = self.get_locator_for_wait(element_page_to['type'], element_page_from['value'])
    #     WebDriverWait(driver, wait).until(ec.presence_of_element_located(element_from_wait))
    #     WebDriverWait(driver, wait).until(ec.presence_of_element_located(element_to_wait))
    #     touch_action = TouchAction(driver)
    #     element_from = self.get_by_mobile(element_page_from['type'],driver, element_page_to['value'])
    #     element_to = self.get_by_mobile(element_page_to['type'], driver, element_page_to['value'])
    #     driver.findElementByAndroidUIAutomator
    #     # logger.info(f'execute {action} with element have is {element_page_to["value"]}')

    from time import sleep
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ec

    def scroll_mobile(self, action, element_destination, driver):
        """
        Scroll to a specific element on the mobile screen based on the provided action.

        :param action: Scroll direction ('up', 'down', 'left', 'right').
        :param element_destination: Dictionary containing type and value of the destination element.
        :param driver: The Appium driver instance.
        """
        try:
            # Get the locator tuple for the destination element
            element = self.get_locator_for_wait(element_destination['type'], element_destination['value'])
            logger.info(f"Retrieved locator for element with value: {element_destination['value']}")
            logger.info(f"Starting to scroll '{action}' to element: {element_destination['value']}")

            # Perform the scroll action
            self.scroll(driver, action, element)

        except KeyError as e:
            logger.error(
                f"KeyError: Missing key in element_destination: {str(e)}. Ensure 'type' and 'value' are provided.")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during scroll. Exception: {str(e)}")
            raise

    def scroll(self, driver, action, element):
        """
        Perform a scroll action in a specified direction until the element is found or a timeout occurs.

        :param driver: The Appium driver instance.
        :param action: Scroll direction ('up', 'down', 'left', 'right').
        :param element: Locator tuple for the destination element.
        :raises: AssertionError if the element is not found after multiple scroll attempts.
        """
        sleep(1)  # Pause to ensure the app is ready for interaction
        flag = False
        max_attempts = 3  # Maximum scroll attempts
        swipe_duration = 2000  # Duration of the swipe in milliseconds
        window_size = driver.get_window_size()

        # Define scroll coordinates for different actions
        scroll_actions = {
            "down": (window_size["width"] / 2, window_size["height"] * 0.6, window_size["width"] / 2,
                     window_size["height"] * 0.3),
            "up": (window_size["width"] / 2, window_size["height"] * 0.3, window_size["width"] / 2,
                   window_size["height"] * 0.6),
            "left": (window_size["width"] * 0.8, window_size["height"] / 2, window_size["width"] * 0.2,
                     window_size["height"] / 2),
            "right": (window_size["width"] * 0.2, window_size["height"] / 2, window_size["width"] * 0.8,
                      window_size["height"] / 2),
        }

        if action not in scroll_actions:
            logger.error(f"Unsupported scroll action: '{action}'")
            raise AssertionError(f"Unsupported scroll action: '{action}'")

        start_x, start_y, end_x, end_y = scroll_actions[action]
        logger.info(f"Scrolling '{action}' with coordinates: start=({start_x}, {start_y}), end=({end_x}, {end_y})")

        # Perform the scroll action
        for attempt in range(1, max_attempts + 1):
            logger.info(f"Scroll attempt {attempt}/{max_attempts}")
            driver.swipe(start_x, start_y, end_x, end_y, swipe_duration)

            try:
                # Wait for the element to become visible
                WebDriverWait(driver, 10).until(ec.presence_of_element_located(element))
                logger.info(f"Element located successfully after {attempt} scroll attempts")
                flag = True
                break
            except Exception as e:
                logger.warning(f"Element not found on attempt {attempt}: {str(e)}")

        if not flag:
            logger.error(f"Failed to locate element after {max_attempts} scroll attempts")
            raise AssertionError(f"Element not found after scrolling {action} {max_attempts} times")

    def close_application(self, driver):
        """
        Safely closes the application if the driver session is active.

        :param driver: The Appium driver instance.
        :raises: AssertionError if the application cannot be closed.
        """
        if driver.session_id:
            try:
                logger.info("Attempting to close the application.")
                driver.quit()
                logger.info("Application closed successfully.")
            except Exception as e:
                logger.error("Failed to close the application. Exception: %s", str(e))
                raise AssertionError("Failed to close the application. Check logs for details.") from e
        else:
            logger.warning("No active session found. The application might already be closed.")






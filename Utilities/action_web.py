import glob
import json
import os
from time import sleep

from selenium.common import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    StaleElementReferenceException, NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from yaml import SafeLoader
from pyshadow.main import Shadow
from libraries.data_generators import check_match_pattern, get_test_data_for
from Utilities.process_value_input import procees_value
from project_runner import logger, project_folder


class ManagementFile:
    SUPPORTED_LOCATOR_TYPES = {
        'ID': By.ID,
        'NAME': By.NAME,
        'XPATH': By.XPATH,
        'LINK TEXT': By.LINK_TEXT,
        'PARTIAL LINK TEXT': By.PARTIAL_LINK_TEXT,
        'CLASS NAME': By.CLASS_NAME,
        'CSS': By.CSS_SELECTOR
    }

    def get_dict_path_yaml(self):
        """
           This function retrieves the paths of all YAML files in the 'resources/pages' directory
           relative to the project folder. It returns a dictionary where the keys are the file names
           and the values are the paths.
           Returns:
               dict: A dictionary where the keys are the file names and the values are the paths.
           """
        file_path = os.path.join(project_folder, "resources", "pages", "*", "*.yaml")
        dict_yaml = {}
        files = glob.glob(file_path, recursive=True)
        for file in files:
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        return dict_yaml

    def read_yaml_file(self, path, page_name, dict_page_element):
        """
    Reads a YAML file and returns the content as a JSON object. If the content for a specific page
    is already cached in dict_page_element, it will return the cached version.

    Args:
        path (str): The path to the YAML file.
        page_name (str): The name of the page.
        dict_page_element (dict): A dictionary containing page elements to cache YAML content.

    Returns:
        dict: The JSON object representing the content of the YAML file.
    """
        try:
            if dict_page_element and page_name in dict_page_element:
                logger.debug(f"Page '{page_name}' found in cache.")
                return dict_page_element[page_name]
            else:
                logger.info(f"Reading YAML file for page '{page_name}' from path: {path}")
                with open(path, encoding='utf-8') as page:
                    python_dict = yaml.load(page.read(), Loader=SafeLoader)
                    if python_dict is None:
                        logger.warning(f"The YAML file for page '{page_name}' is empty or invalid.")
                        return {}
                    # Convert Python dictionary to JSON object
                    json_result = json.dumps(python_dict, default=str)
                    json_object = json.loads(json_result)
                    dict_page_element[page_name] = json_object
                    logger.info(f"YAML file for page '{page_name}' loaded and cached successfully.")
                    return json_object
        except FileNotFoundError as e:
            print(f"Error: The YAML file for '{page_name}' could not be found.")
            logger.error(f"File '{path}' not found for page '{page_name}': {e}")
            return {}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file for page '{page_name}': {e}")
            print(f"Error: The YAML file for '{page_name}' could not be parsed. Please check its syntax.")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error converting YAML to JSON for page '{page_name}': {e}")
            print(f"Error: There was an issue converting the YAML file to JSON for '{page_name}'.")
            return {}
        except Exception as e:
            # Generic error catch for unexpected issues
            logger.error(f"Unexpected error while reading YAML file for page '{page_name}': {str(e)}")
            print(f"Error: An unexpected error occurred while reading the YAML file for '{page_name}'.")
            return {}

    def get_element_by(self, type: str, driver, value: str) -> WebElement:
        """
        Find and return a WebElement based on the given type and value.

        Args:
            type (str): The type of locator to use. Supported types are 'id', 'name', 'xpath', 'link_text',
                        'partial_link_text', 'class_name', and 'css_selector'.
            driver (WebDriver): The WebDriver instance to use for finding the element.
            value (str): The value to use for finding the element.

        Returns:
            WebElement: The found WebElement.

        Raises:
            ValueError: If the given type is not supported.
            NoSuchElementException: If the element is not found.
            TimeoutException: If the element is not found within the specified timeout.
            Exception: If there is an error locating the element.
        """
        # Check if the locator type is valid
        logger.info(f'Getting list element by {type} with value is {value}')
        locator = self.SUPPORTED_LOCATOR_TYPES.get(type)
        if not locator:
            logger.error(f"Invalid locator type: {type}. Supported types are 'id', 'name', 'xpath', 'link_text', "
                         "'partial_link_text', 'class_name', 'css_selector'.")
            raise ValueError(f"Invalid locator type: {type}. Supported types are 'id', 'name', 'xpath', 'link_text', "
                             "'partial_link_text', 'class_name', 'css_selector'.")
        try:
            logger.info(f'Get element by {type} with value is {value}')
            return driver.find_element(locator, value)
        except NoSuchElementException:
            logger.error(f"No such element found using {type} with value: {value}.")
            return None  # Return None to indicate that the element could not be located
        except Exception as e:
            logger.error(f"Error locating element by {type} with value '{value}': {str(e)}")
            return None  # Return None for unexpected errors, ensuring the process continues

    def get_list_element_by(self, type, driver, value):
        try:
            logger.info(f'Getting list element by {type} with value is {value}')
            locator = self.SUPPORTED_LOCATOR_TYPES.get(type)
            if locator is None:
                raise ValueError(
                    f"Invalid locator type: {type}. Supported types are 'id', 'name', 'xpath', 'link_text', 'partial_link_text', 'class_name', and 'css_selector'.")
            return driver.find_elements(locator, value)
        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
            return None
        except Exception as e:
            print(f"Error locating element: {str(e)}")
            return None

    def get_locator_for_wait(self, type, value):
        logger.info(f'getting locator for wait with type {type} with value is {value}')
        try:
            logger.info(f'Getting locator for wait with type {type} with value is {value}')
            locator = self.SUPPORTED_LOCATOR_TYPES.get(type)
            if locator is None:
                raise ValueError(
                    f"Invalid locator type: {type}. Supported types are 'id', 'name', 'xpath', 'link_text', 'partial_link_text', 'class_name', and 'css_selector'.")
            return locator, value
        except Exception as e:
            raise Exception(f"Error locating element: {str(e)}")

    def get_locator(self, element_page, device):
        """
            A function to get the locator based on the element page and device provided.

            Args:
                self: The object itself.
                element_page: The element page to get the locator from.
                device: The device to get the locator for.

            Returns:
                The locator for the specified element page and device.
            """
        try:
            locators = [locator for locator in element_page.get_list_locator() if locator.get_device() == device]
            if not locators:
                raise ValueError(f"No locators found for device: {device}")
            logger.info(f"Locator found for device '{device}' and element page '{element_page}'.")
            return locators[0]
        except ValueError as e:
            logger.error(f"ValueError in get_locator: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_locator: {str(e)}")
            raise ValueError(f"Error getting locator for device '{device}' and element page '{element_page}': {str(e)}")

    def get_locator_from_action(self, element_page, device):
        """
        A function to get the locator from the element page based on the provided device.

        Args:
            element_page (dict): The element page containing locators.
            device (str): The device to get the locator for.

        Returns:
            dict: The locator for the specified device.

        Raises:
            ValueError: If the 'locators' key is not found in the element_page.
            TypeError: If the 'device' is not of the expected type.
        """
        # Validate input types
        if not isinstance(element_page, dict):
            logger.error("Invalid element_page: Expected a dictionary.")
            raise TypeError("Expected element_page to be a dictionary.")
        if not isinstance(device, str):
            logger.error(f"Invalid device type: {type(device)}. Expected a string.")
            raise TypeError("Expected device to be a string.")

        # Check if 'locators' key exists in the element_page
        if 'locators' not in element_page:
            logger.error(f"Element page does not contain 'locators' key: {element_page}")
            raise ValueError("The element_page must contain a 'locators' key.")

        try:
            logger.info(f"Searching for locator for device '{device}' in element page.")
            # Search for the locator corresponding to the device
            locator = next(locator for locator in element_page['locators'] if locator['device'] == device)
            logger.info(f"Locator found for device '{device}'.")
            return locator
        except StopIteration:
            # If no locator is found, log and return None
            logger.warning(f"No locator found for device '{device}' in element page.")
            return None
        except Exception as e:
            # Log any unexpected errors
            logger.error(f"Error occurred while retrieving locator for device '{device}': {str(e)}")
            raise

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def get_shadow_element(self, locator_type, driver, locator_value, wait, is_highlight):
        """
        Finds a shadow DOM element based on the provided parameters.

        Args:
            locator_type (str): The type of locator. Must be 'CSS' or 'XPATH'.
            driver (WebDriver): The WebDriver instance.
            locator_value (str): The value used to locate the shadow element.
            wait (int): The time in seconds to wait for the shadow element to appear.
            is_highlight (bool): Whether to highlight the shadow element.

        Returns:
            WebElement: The located shadow element.

        Raises:
            ValueError: If the locator_type is invalid.
            NoSuchElementException: If the shadow element cannot be found.
        """
        logger.info(f'Attempting to locate shadow element: {locator_value} with type: {locator_type}')

        valid_types = {'CSS', 'XPATH'}
        if locator_type not in valid_types:
            logger.error(f"Invalid locator type: {locator_type}. Supported types: {valid_types}")
            raise ValueError(f"Locator type must be one of {valid_types}. Received: {locator_type}")

        # Create Shadow instance and configure explicit wait
        shadow = Shadow(driver)
        shadow.set_explicit_wait(wait, polling_interval=0.2)

        try:
            element = self._find_shadow_element(shadow, locator_type, locator_value)
            if is_highlight:
                shadow.highlight(element, color='red', time_in_mili_seconds=0.2)
            logger.debug(f'Shadow element located successfully: {locator_value}')
            return element
        except NoSuchElementException:
            logger.error(f"Shadow element not found: {locator_value}")
            raise NoSuchElementException(f"Could not locate shadow element: {locator_value}")
        except Exception as e:
            logger.error(f"An error occurred while locating shadow element: {locator_value}. Error: {str(e)}")
            raise

    def _find_shadow_element(self, shadow, locator_type, locator_value):
        """Find the shadow element using the specified locator type."""
        if locator_type == 'CSS':
            return shadow.find_element(locator_value, False)
        elif locator_type == 'XPATH':
            return shadow.find_element_by_xpath(locator_value, False)
    def action_with_shadow_element(self, element_page, action, driver, value, wait, dict_save_value, is_highlight):
        """
            Perform actions on a shadow element.
            Args:
                element_page (dict): The page element containing type and value.
                action (str): The action to be performed.
                driver (WebDriver): The WebDriver instance.
                value (str): The value to be used in the action.
                wait (int): The wait time in seconds.
                dict_save_value (dict): The dictionary to get value from.
                is_highlight (bool): Whether to highlight the element.
            Raises:
                NoSuchElementException: If the shadow element is not found.
                TimeoutException: If waiting for the element times out.
                Exception: If any other error occurs.
            """
        try:
            if value:
                value = procees_value().get_value(value, dict_save_value)
                value = get_test_data_for(value, dict_save_value)
            element = self.get_shadow_element(element_page['type'], driver, element_page['value'], wait, is_highlight)
            logger.info(f'Executing {action} on element: {element_page["value"]}')
            if action == "click":
                element.click()
            elif action == "type":
                if dict_save_value:
                    value = dict_save_value.get(value, value)
                element.send_keys(value)
            elif action == "clear":
                element.clear()
            elif action == "wait":
                # The current framework only supports waiting for elements with status set to ENABLED.
                # This restriction ensures that elements are fully loaded and interactive before proceeding with actions.
                # Future updates may include support for additional statuses like DISABLED or HIDDEN based on requirements and use cases.
                WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
            else:
                logger.error(f"Unsupported action: {action}")
                raise ValueError(f"Unsupported action: {action}")
        except NoSuchElementException as e:
            logger.error(f"Element not found: {e}")
            raise
        except TimeoutException as e:
            logger.error(f"Timeout waiting for element: {e}")
            raise TimeoutException(f"Timeout waiting for element: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise Exception(f"An error occurred: {e}")

    def action_mouse(self, action, element_page_from, element_page_to, context):
        """
            Performs a mouse action on web elements.
            Args:
                action (str): The action to be performed.
                element_from (dict): The source element containing type and value.
                element_to (dict): The target element containing type and value.
                context (object): The context object containing the driver.
            Raises:
                AssertionError: If the action is not supported.
            """
        element_from = self.get_element_by(element_page_from['type'], context.driver, element_page_from['value'])
        logger.info(f'Executing {action} with element have is {element_page_from["value"]}')
        if action == 'drag-and-drop':
            action = ActionChains(context.driver)
            element_to = self.get_element_by(element_page_to['type'], context.driver, element_page_to['value'])
            logger.info(f'execute {action} with element have is {element_page_to["value"]}')
            action.drag_and_drop(element_from, element_to).perform()
        else:
            logger.error("Can not execute %s with element have is %s", action)
            assert False, f"Unsupported action: {action}"

    def handle_popup(self, driver, status, wait):
        """
        Handles a popup dialog on a web page.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            status (str): The desired action for the popup dialog ('accept' or 'dismiss').
            wait (int): The maximum time to wait for the popup to appear, in seconds.

        Raises:
            ValueError: If the provided status is unsupported.
            AssertionError: If no alert is present or other errors occur.
        """
        logger.info(f"Attempting to handle popup with status '{status}'.")

        # Validate the provided status
        supported_statuses = {'accept', 'dismiss'}
        if status not in supported_statuses:
            logger.error(f"Unsupported status: '{status}'. Supported statuses: {supported_statuses}")
            raise ValueError(f"Unsupported status: '{status}'. Supported statuses: {supported_statuses}")

        try:
            # Wait for the alert to be present
            WebDriverWait(driver, wait).until(ec.alert_is_present(), "Timed out waiting for alert to appear.")
            alert = driver.switch_to.alert
            logger.info(f"Popup detected: '{alert.text.strip()}' (if available).")

            # Handle the alert based on the specified status
            if status == 'accept':
                alert.accept()
                logger.info("Popup accepted successfully.")
            elif status == 'dismiss':
                alert.dismiss()
                logger.info("Popup dismissed successfully.")

        except TimeoutException:
            logger.error("Timed out waiting for alert to appear.")
            raise AssertionError("No alert present within the specified wait time.")
        except NoAlertPresentException:
            logger.error("No alert present when attempting to switch.")
            raise AssertionError("No alert present to handle.")
        except Exception as e:
            logger.error(f"Unexpected error while handling popup: {str(e)}")
            raise AssertionError(f"Unexpected error while handling popup: {str(e)}")

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
            Reads a YAML file and returns the content as a JSON object.

            Args:
                path (str): The path to the YAML file.
                page_name (str): The name of the page.
                dict_page_element (dict): A dictionary containing page elements.

            Returns:
                json: The JSON object representing the content of the YAML file.
            """
        try:
            if dict_page_element and page_name in dict_page_element.keys():
                obj_page = dict_page_element[page_name]
                return obj_page
            else:
                with open(path, encoding='utf-8') as page:
                    python_dict = yaml.load(page.read(), Loader=SafeLoader)
                    json_result = json.dumps(python_dict)
                    json_object = json.loads(json_result)
                    dict_page_element[page_name] = json_object
                    return json_object
        except FileNotFoundError:
            print(f"File '{page_name}' not found.")
            logger.error(f"File '{page_name}' not found.")
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            print(f"Error reading YAML file: {str(e)}")
            logger.error(f"Error reading YAML file: {str(e)}")

    def get_element_by(self, type, driver, value) -> WebElement:
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
        logger.info(f'Getting list element by {type} with value is {value}')
        locator = self.SUPPORTED_LOCATOR_TYPES.get(type)
        if locator is None:
            raise ValueError(
                f"Invalid locator type: {type}. Supported types are 'id', 'name', 'xpath', 'link_text', 'partial_link_text', 'class_name', and 'css_selector'.")

        try:
            logger.info(f'Get element by {type} with value is {value}')

            locator = self.SUPPORTED_LOCATOR_TYPES.get(type)
            return driver.find_element(locator, value)
        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Element not found: {str(e)}")
            assert False, f"Element not found: {str(e)}"
        except Exception as e:
            logger.error(f"Error locating element: {str(e)}")
            assert False, f"Error locating element: {str(e)}"

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
            locators = [locator for locator in element_page.get_list_locator() if locator.get_device().__eq__(device)]
            if not locators:
                raise ValueError(f"No locators found for device: {device}")
            return locators[0]
        except Exception as e:
            raise ValueError(f"Error getting locator: {str(e)}")

    def get_locator_from_action(self, element_page, device):
        """
          A function to get the locator from the element page based on the provided device.
          Args:
              self: The object itself.
              element_page (dict): The element page containing locators.
              device (str): The device to get the locator for.
          Returns:
              dict: The locator for the specified device.
          """
        try:
            return next(locator for locator in element_page['locators'] if locator['device'] == device)
        except StopIteration:
            return None

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def process_execute_action(self, driver, wait, element, type_action, value, locator, action_elements,
                               dict_save_value):
        """
            Process and execute an action on a web element.
            Args:
                driver (WebDriver): The web driver instance.
                wait (int): The wait time in seconds.
                element (WebElement): The web element to interact with.
                type_action (str): The type of action to perform ('click' or 'text').
                value (str): The value to send to the element (if type_action is 'text').
                locator (dict): The locator of the element.
                action_elements (list): The list of action elements.
            Raises:
                TimeoutException: If the element is not clickable within the specified wait time.
                Exception: If an error occurs during action execution.
            """
        try:
            value = procees_value().get_value(value, dict_save_value)
            logger.info(f'execute action  {type_action} with element have value {locator}')
            WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
            if type_action == 'click':
                if element.get_attribute("disabled") is None:
                    element.click()
                else:
                    WebDriverWait(driver, wait).until_not(
                        ec.element_attribute_to_include(
                            self.get_locator_for_wait(locator[type], locator['value']), "disabled"))
                    element.click()
            elif type_action == "text":
                element.send_keys(value)
            else:
                self.wait_for_action(action_elements, wait, driver, element, locator)
        except TimeoutException:
            logger.error(f'Timeout waiting for element to be clickable: {locator}')
        except Exception as e:
            logger.error(f'An error occurred during action execution: {str(e)}')

    # def check_field_exist(self, dict, key):
    #     try:
    #         if dict[key]:
    #             return True
    #     except Exception as e:
    #         print(f'not found attribute in dictionary: {str(e)}')
    #         return False

    def wait_for_action(self, action_elements, wait, driver, element, locator):
        """
        Wait for a specific action on a web element based on the given conditions.

        Args:
            action_elements (dict): Dictionary containing the condition for the action.
            wait (int): The wait time in seconds.
            driver (WebDriver): The web driver instance.
            element (WebElement): The web element to interact with.
            locator (dict): The locator of the element.

        Raises:
            TimeoutException: If the condition is not met within the specified wait time.
            Exception: If an error occurs during action execution.
        """
        locator_from_wait = self.get_locator_for_wait(locator['type'], locator['value'])
        supported_conditions = ["ENABLED", "NOT_ENABLED", "DISPLAYED", "NOT_DISPLAYED", "EXISTED", "NOT_EXISTED",
                                "SELECTED", "NOT_SELECTED"]
        try:
            condition = action_elements.get('condition')
            if condition not in supported_conditions:
                raise ValueError(f"Unsupported condition: {condition}")

            if condition in ["ENABLED", "DISPLAYED", "EXISTED", "SELECTED"]:
                WebDriverWait(driver, wait).until(
                    self.get_expected_condition(driver, condition, locator_from_wait))
            elif condition in ["NOT_ENABLED", "NOT_DISPLAYED", "NOT_EXISTED", "NOT_SELECTED"]:
                WebDriverWait(driver, wait).until_not(
                    self.get_expected_condition(driver, condition[4:], locator_from_wait))
            else:
                raise ValueError(f"Unsupported condition: {condition}")
        except (TimeoutException, ValueError) as e:
            error_message = f"Failed to wait for action with condition '{condition}' on element: {locator}. Error: {str(e)}"
            logger.error(error_message)
            raise TimeoutException(error_message)
        except Exception as e:
            error_message = f"An error occurred during action execution on element: {locator}. Error: {str(e)}"
            logger.error(error_message)
            raise Exception(error_message)

    def get_expected_condition(self, driver, condition, locator):
        """
          Get the expected condition based on the given condition type and locator.
          Args:
              driver (WebDriver): The web driver instance.
              condition (str): The type of condition to check.
              locator (dict): The locator information for the element.
          Returns:
              ExpectedCondition: The expected condition based on the input.
          Raises:
              ValueError: If the condition type is not supported.
          """
        if condition == "ENABLED":
            return ec.element_to_be_clickable(locator)
        elif condition == "DISPLAYED":
            return ec.presence_of_element_located(locator)
        elif condition == "EXISTED":
            return lambda driver: len(self.get_list_element_by(locator['type'], driver, locator['value'])) > 0
        elif condition == "SELECTED":
            return ec.element_located_to_be_selected(locator)
        else:
            raise ValueError(f"Unsupported condition: {condition}")

    def get_shadow_element(self, type, driver, value, wait, is_highlight):
        """
            This method finds a shadow element based on the provided type, driver, value, wait, and highlight settings.
            Args:
                type (str): The type of the shadow element. It should be either 'CSS' or 'XPATH'.
                driver (WebDriver): The webdriver instance.
                value (str): The value used to locate the shadow element.
                wait (int): The time to wait for the shadow element to appear.
                is_highlight (bool): Whether to highlight the shadow element.
            Returns:
                WebElement: The found shadow element.
            Raises:
                AssertionError: If the type of shadow element is not 'CSS'.
            """
        logger.info(f'Finding shadow element {value}')

        shadow = Shadow(driver)
        shadow.set_explicit_wait(wait, 0.2)
        try:
            if type == 'CSS':
                element = shadow.find_element(value, False)
            elif type == 'XPATH':
                element = shadow.find_element_by_xpath(value, False)
            else:
                logger.error(f'The type of shadow element must be CSS or XPATH, type is {type}')
                raise AssertionError(f'The type of shadow element must be CSS or XPATH')
            if is_highlight:
                shadow.highlight(element, color='red', time_in_mili_seconds=0.2)
            logger.debug(f'Shadow element {value} found')
            return element
        except NoSuchElementException:
            logger.error(f'Shadow element {value} not found')
            raise NoSuchElementException(f'Shadow element {value} not found')

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
               status (str): The desired status of the popup dialog.
               wait (int): The wait time in seconds.
           Raises:
               AssertionError: If the status is not supported.
           """
        try:
            alert = driver.switch_to.alert
            WebDriverWait(driver, wait).until(ec.alert_is_present(), 'Timed out waiting for simple alert to appear')
            if status == 'accept':
                alert.accept()
            elif status == 'dismiss':
                alert.dismiss()
            else:
                logger.error("Unsupported status: %s", status)
                assert False, "Not supported status in framework"
        except NoAlertPresentException:
            logger.error("No alert present")
            assert False, "No alert present"
        except Exception as e:
            logger.error(f"Failed to handle popup: {e}")
            assert False, f"Failed to handle popup: {e}"

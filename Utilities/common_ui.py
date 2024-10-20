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

    def action_page(self, element_page, action, driver, value, wait, dict_save_value, device, context):
        element = self.get_element_by_from_device(element_page, device, driver)
        logger.info(f'execute {action} with element have is {element_page["value"]}')
        self.highlight(element, 0.3, context.highlight)
        if value:
            value = procees_value().get_value(value, dict_save_value)
            value = get_test_data_for(value, dict_save_value)
        try:
            if action.__eq__("click"):
                self.click_action(element, wait, element_page, device, driver)
            elif action.__eq__('double-click'):
                action_chains = ActionChains(driver)
                action_chains.double_click(on_element=element)
                action_chains.perform()
            elif action.__eq__('right-click'):
                action_chains = ActionChains(driver)
                action_chains.context_click(on_element=element)
                action_chains.perform()
            elif action.__eq__('select'):
                Select(element).select_by_visible_text(value)
            elif action.__eq__("type"):
                element.send_keys(value)
            elif action.__eq__("text"):
                element.send_keys(value)
            elif action.__eq__("clear"):
                element.clear()
            elif action.__eq__('hover-over'):
                self.mouse_action(element, driver, action, device)
            else:
                logger.error("Can not execute %s with element have is %s", action)
                assert False, "Not support action in framework"
        except (ElementNotInteractableException, StaleElementReferenceException):
            self.handle_element_not_interactable_exception(value, wait, element_page, device, driver, action,
                                                           count_number=0)
        except (InvalidElementStateException):
            self.handle_invalid_element_state_exception(value, element_page, device, driver, action)
        except Exception as e:
            logger.info(f"do not {action} with element {element} trying to {action} by javascript")
            logger.error(e)
            try:
                driver.execute_script("arguments[0].%s(arguments[1]);" % action, element, value)
            except:
                logger.error(f"do not {action} with element {element} by javascript")
                assert False, f"do not {action} with element {element}"

    def click_action(self, element, wait, element_page, device, driver):
        if element_page['device'] == "WEB":
            try:
                if element.get_attribute("disabled") is None:
                    element.click()
                else:
                    WebDriverWait(driver, wait).until_not(
                        ec.element_attribute_to_include(
                            ManagementFile().get_locator_for_wait(element_page['type'], element_page['value']),
                            "disabled"))
                    element.click()
            except (ElementNotInteractableException, StaleElementReferenceException):
                self.handle_element_not_interactable_exception("", wait, element_page, device, driver, "click", 1)
            except (ElementClickInterceptedException):
                sleep(1)
                element.click()
            except Exception as e:
                logger.info(f"do not click with element {element} trying to click by javascript")
                logger.error(e)
                try:
                    driver.execute_script("arguments[0].click();", element)
                except:
                    logger.error(f"do not click with element {element} by javascript")
                    assert False, f"do not click with element {element}"
        else:
            locator_from_wait = ManagementFileAndroid().get_locator_for_wait(element_page['type'],
                                                                             element_page['value'])
            WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator_from_wait))
            element.click()

    def wait_element_for_status(self, element_page, status, driver, device, wait, flag):
        """
           Waits for an element to have a specific status.
           Args:
               element_page (dict): The element page specification.
               status (str): The desired status of the element.
               driver (WebDriver): The Selenium WebDriver instance.
               device (dict): The device information.
               wait (int): The wait time in seconds.
           Raises:
               AssertionError: If the element does not have the expected status.
               ValueError: If the status is not supported.
           """
        # Get the locator for waiting
        locator_from_wait = self.get_locator_for_wait_from_device(element_page)
        logger.info(f"Waiting for element '{element_page['value']}' to have status '{status}'")
        try:
            if status == "DISPLAYED":
                WebDriverWait(driver, wait).until(ec.visibility_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, wait).until(ec.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, wait).until(ec.element_to_be_clickable(locator_from_wait))
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, wait).until_not(ec.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by_from_device(element_page, device, driver)
                WebDriverWait(driver, wait).until(lambda ele: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by_from_device(element_page, device, driver)
                WebDriverWait(driver, wait).until(lambda ele: len(elements) == 0)
            elif status == "SELECTED":
                WebDriverWait(driver, wait).until(ec.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, wait).until_not(ec.element_located_to_be_selected(locator_from_wait))
            else:
                raise ValueError(f"Unsupported status: {status}")
            return "PASS"
        except Exception as e:
            logger.info(f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}")
            assert flag, f"Failed to wait for element '{element_page['value']}' to have status '{status}': {str(e)}"
            if flag:
                return "SKIP"

    def get_element(self, page, element, platform_name, dict_save_value):
        """
           This function retrieves the locator for a given element from a page specification.

           Args:
               page (dict): The page specification.
               element (str): The element to retrieve the locator for.
               platform_name (str): The platform for which the locator is needed.
               dict_save_value (dict): A dictionary of values to be used for substitution in the locator.
           Returns:
               dict: The locator for the given element.
           Raises:
               AssertionError: If the element does not exist in the page spec.
           """
        # Initialize text variable
        text = ""
        # Check if the element has a text condition
        if "with text" in element:
            arr_value = element.split("with text")
            # remove blank in array
            arr_value = [i.lstrip() for i in arr_value]
            element = arr_value[0].strip()
            # remove double quote
            text = arr_value[1].replace('"', '')
            if dict_save_value:
                text = dict_save_value.get(text, text)
            page_temp = copy.deepcopy(page)
        else:
            page_temp = page
        # Find the element in the page spec
        element_spec = next((el for el in page_temp['elements'] if el['id'] == element), None)
        if element_spec is None:
            logger.error(f'Element {element} not found in page spec, with platform {platform_name}')
            raise ValueError(f'Element {element} not found in page spec, with platform {platform_name}')

        # Find the locator for the specified platform
        locator = next((loc for loc in element_spec['locators'] if loc['device'] == platform_name), None)
        if locator is None:
            logger.error(f'Locator for element {element} not found for platform {platform_name}')
            raise ValueError(f'Locator for element {element} not found for platform {platform_name}')

        # Substitute the text in the locator value
        locator['value'] = locator['value'].replace("{text}", text)

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
                element_yaml = self.get_element(page, arr_element[0]['id'] + " with text " + value, platform_name,
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
                value = re.search(pattern, value).group(0)
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
                    return element.get_attribute('value')
                else:
                    # If the element is not an input tag, return its text content
                    return element.text

            except (ElementNotInteractableException, StaleElementReferenceException):
                self.handle_element_not_interactable_exception("", None, element_page, device, driver, "get_value")
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
                                         is_highlight):
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
            raise AssertionError(f'Element with ID {row[0]} not found in the page')

        logger.info(f'Verifying for {row[0]} have value {row[1]} and status {row[2]}')
        value = row[1]
        helper = row[3]
        if value is None:
            value = ''
        else:
            value = procees_value().get_value(value, dict_save_value)

        element_yaml = self.get_element(page, arr_element[0]['id'] + " with text " + value, platform_name,
                                        dict_save_value)
        if not element_yaml:
            raise AssertionError(f'Element with ID {row[0]} and value {value} not found in the page')

        if row[2] and element_yaml:
            if value != '' and helper is None:
                logger.info(f'Verified for {row[0]} have value {row[1]} and status {row[2]}')
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
            assert value == expect, f'value of the element is {value} not equal to values expected {expect}'
        except NoSuchElementException:
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
            assert False, f'The helper and value columns must both have a value at the same time'

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
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
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
                    driver.execute_script(
                        "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });",
                        element)
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
            print('An error occurred while executing action with keyboard:', key_action)
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
            print('fail when execute javascript file', e)
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
            print('fail when execute javascript file', e)
            assert False, f"fail when execute javascript file {javascript_file}"

    def handle_element_not_interactable_exception(self, value, wait, element_page, device, driver, action,
                                                  count_number):
        element = self.get_element_by_from_device(element_page, device, driver)
        try:
            if device['platformName'] == "WEB":
                driver.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });", element)
        except Exception as e:
            assert True, f"fail when scroll to element {element}, skip step scroll to element"
        match action:
            case "click":
                try:
                    for count_number in range(10):
                        sleep(1)
                        self.click_action(element, wait, element_page, device, driver)
                        break
                except (ElementNotInteractableException, StaleElementReferenceException):
                    self.handle_element_not_interactable_exception(value, wait, element_page, device, driver, action,
                                                                   count_number+1)
            case "type":
                try:
                    for count_number in range(10):
                        sleep(1)
                        logger.info(f"perform with action type {value} and count {count_number}")
                        element.send_keys(value)
                        break
                except (ElementNotInteractableException, StaleElementReferenceException):
                    self.handle_element_not_interactable_exception(value, wait, element_page, device, driver, action, count_number+1)
            case "text":
                try:
                    for count_number in range(10):
                        sleep(1)
                        element.send_keys(value)
                        break
                except (ElementNotInteractableException, StaleElementReferenceException):
                    self.handle_element_not_interactable_exception(value, wait, element_page, device, driver, action, count_number+1)
            case "get_value":
                try:
                    for count_number in range(10):
                        if element.get_attribute("value") and element.tag_name.lower() == "input":
                            return element.get_attribute('value')
                        else:
                            # If the element is not an input tag, return its text content
                            return element.text
                except (ElementNotInteractableException, StaleElementReferenceException):
                    self.handle_element_not_interactable_exception(value, wait, element_page, device, driver, action, count_number+1)
            case _:
                print(f'not exist {action} in element not interactable exception')
                assert False, f"not exist {action} in element not interactable exception"
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
                print(f'not exist {action} in element not interactable exception')
                assert False, f"not exist {action} in element not interactable exception"

    def execute_action(self, page, action_id, driver, wait, table, dict_save_value, platform_name, context):
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
            Returns:
                None
            Raises:
                AssertionError: If the action or element cannot be executed.
                FileNotFoundError: If the page file is not found.
                YAMLError: If there is an error reading the YAML file.
                :param context:
            """
        dict_action = page['actions']
        dict_action = list(filter(
            lambda action: action['id'] == action_id, dict_action
        ))
        type_action = None
        result = True
        if dict_action:
            obj_action = dict_action[0]
            arr_list_action = obj_action['actionElements']
            for action_elements in arr_list_action:
                value=""
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
                            if type_action in ["click", "text"]:
                                self.action_page(locator, type_action, driver, value, action_elements['timeout'],
                                                 dict_save_value, platform_name, context)
                            else:
                                self.action_page(locator, "text", driver, type_action, action_elements['timeout'],
                                                 dict_save_value, platform_name, context)
                    except Exception as e:
                        logger.info(f'can not execute action with element have value  {locator} in framework')
                        assert False, "can not execute action with element have value" + locator + "in framework"
                elif self.check_field_exist(action_elements, 'condition') and self.check_field_exist(action_elements,
                                                                                                     'timeout') is False:
                    try:
                        self.wait_element_for_status(locator, action_elements['condition'], driver, platform_name, wait,
                                                     False)
                        if self.check_field_exist(action_elements, 'inputType'):
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text"]:
                                self.action_page(locator, type_action, driver, value, wait, dict_save_value,
                                                 platform_name, context)
                            else:
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value, platform_name,
                                                 context)
                        else:
                            self.wait_element_for_status(locator, action_elements['condition'], driver, platform_name,
                                                         wait, False)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator['value'])
                        assert False, "can not execute action " + type_action + " with element have value" + locator[
                            'value'] + "in framework"
                else:
                    try:
                        if self.check_field_exist(action_elements, 'inputType'):
                            type_action = action_elements['inputType']
                            if type_action in ["click", "text"]:
                                self.action_page(locator, type_action, driver, value, wait, dict_save_value,
                                                 platform_name, context)
                            else:
                                self.action_page(locator, "text", driver, type_action, wait, dict_save_value, platform_name,
                                                 context)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator.value)
                        assert False, "can not execute action " + type_action + " with element have value" + locator.value + "in framework"
        else:
            logger.error(f'Not Found Action {action_id} in page yaml')
            assert False, "Not Found Action " + action_id + " in page yaml"

    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except Exception as e:
            print(f'not found attribute in dictionary: {str(e)}')
            return False

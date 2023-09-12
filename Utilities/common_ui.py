from time import sleep

from faker import Faker
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from Utilities.action_android import ManagementFileAndroid
from Utilities.action_web import ManagementFile
from libraries.faker import management_user
from libraries.faker.User import generate_user
from project_runner import logger
from selenium.webdriver.support.color import Color
from libraries.data_generators import check_match_pattern


class common_device:
    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def action_page(self, element_page, action, driver, value, wait, dict_save_value, device, context):
        element = self.get_element_by_from_device(element_page, device, driver)
        logger.info(f'execute {action} with element have is {element_page["value"]}')
        # WebDriverWait(driver, wait).until(ec.all_of(
        #     ec.element_to_be_clickable(element))
        # )
        self.highlight(element,  0.3, context.highlight)
        if action.__eq__("click"):
            self.click_action(element, wait, element_page, device, driver)
        elif action.__eq__("type"):
            if dict_save_value:
                if 'USER.' in value:
                    value = self.get_value_from_user_random(value, dict_save_value)
                else:
                    value = dict_save_value.get(value, value)
            element.send_keys(value)
        elif action.__eq__("clear"):
            element.clear()
        elif action.__eq__('hover-over'):
            action = ActionChains(driver)
            action.move_to_element(element).perform()
        else:
            logger.error("Can not execute %s with element have is %s", action)
            assert False, "Not support action in framework"

    def click_action(self, element, wait, element_page, device, driver):
        if device['platformName'] == "WEB":
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(
                        ManagementFile().get_locator_for_wait(element_page['type'], element_page['value']),
                        "disabled"))
                element.click()
        else:
            locator_from_wait = ManagementFileAndroid().get_locator_for_wait(element_page['type'],
                                                                             element_page['value'])
            WebDriverWait(driver, wait).until(
                ec.element_to_be_clickable(locator_from_wait))
            element.click()

    def wait_element_for_status(self, element_page, status, driver, device, wait):
        # locator = ManagementFile().get_locator(element_page, wait)
        locator_from_wait = self.get_locator_for_wait_from_device(element_page, device)
        logger.info(f"wait element have value {element_page['value']} with the status {status}")
        try:
            if status == "DISPLAYED":
                WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator_from_wait))
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
                WebDriverWait(driver, wait).until_not(lambda ele: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, wait).until(ec.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, wait).until_not(ec.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except Exception as e:
            logger.error(f"The status {status['value']} is not currently.  with element have value {element_page['value']}")
            assert False, e

    def get_element(self, page, element, platform_name, dict_save_value):
        text = ""
        if "with text" in element:
            arr_value = element.split("with text")
            # remove blank in array
            arr_value = [i.lstrip() for i in arr_value]
            element = arr_value[0].strip()
            # remove double quote
            text = arr_value[1].replace('"','')
            if dict_save_value:
                text = dict_save_value.get(text, text)
        arr_element = page['elements']
        arr_element = list(filter(
            lambda loc: loc['id'] == element, arr_element
        ))
        try:
            arr_locator = arr_element[0]['locators']
        except IndexError:
            arr_locator = 'null'
            assert False, f'element {element} not exist in page spec'
        arr_locator = list(filter(
            lambda loc: loc['device'] == platform_name, arr_locator
        ))
        arr_locator[0]['value'] = arr_locator[0]['value'].replace("{text}", text)
        return arr_locator[0]

    def verify_elements_with_status(self, page, table, platform_name, dict_save_value, driver, device, wait):
        # arr_element = page['elements']
        if table is not None:
            for row in table:
                arr_element = page['elements']
                arr_element = list(filter(
                    lambda element: element['id'] == row["Field"], arr_element
                ))
                logger.info(f'Verifying for {row["Field"]} have value {row["Value"]} and status {row["Status"]}')
                value = row["Value"]
                if dict_save_value:
                    value = dict_save_value.get(value, value)
                element_yaml = self.get_element(page, arr_element[0]['id'] + " with text " + value, platform_name,
                                                dict_save_value)
                self.wait_element_for_status(element_yaml, row["Status"], driver, device, wait)
                logger.info(f'Verified for {row["Field"]} have value {row["Value"]} and status {row["Value"]}')
        else:
            logger.error("user must set data table for elements")
            assert False, "can not execute verify status for elements"

    def save_text_from_element(self, element_page, driver, key, dict_save_value, wait, device):
        try:
            # locator = ManagementFile().get_locator(element_page, device['platformName'])
            logger.info(f"save text for element {element_page['value']} with key is {key}")
            WebDriverWait(driver, wait).until(
                ec.presence_of_element_located(self.get_locator_for_wait_from_device(element_page, device)))
            element = self.get_element_by_from_device(element_page, device, driver)
            value = self.get_value_element_form_device(element, device)
            dict_save_value["KEY." + key] = value
            return dict_save_value
        except Exception as e:
            logger.error(f"Can not save text for element {element_page['value']} with key is {key}")
            assert False, "Can not save text for element " + element_page['value']
    def save_coordinates_from_element(self, element_page, driver, key, dict_save_value, wait, device):
        try:
            # locator = ManagementFile().get_locator(element_page, device['platformName'])
            logger.info(f"save coordinates for element {element_page['value']} with key is {key}")
            WebDriverWait(driver, wait).until(
                ec.presence_of_element_located(self.get_locator_for_wait_from_device(element_page, device)))
            element = self.get_element_by_from_device(element_page, device, driver)
            location = element.location
            dict_save_value["KEY." + key] = location
            return dict_save_value
        except Exception as e:
            logger.error(f"Can not save coordinates for element {element_page['value']} with key is {key}")
            assert False, "Can not save coordinates for element " + element_page['value']

    def get_locator_for_wait_from_device(self, element_page, device):
        if device['platformName'] == "WEB":
            return ManagementFile().get_locator_for_wait(element_page['type'], element_page['value'])
        else:
            return ManagementFileAndroid().get_locator_for_wait(element_page['type'], element_page['value'])

    def get_list_element_by_from_device(self, element_page, device, driver):
        if device['platformName'] == "WEB":
            return ManagementFile().get_list_element_by(element_page['type'], driver, element_page['value'])
        else:
            return ManagementFileAndroid().get_list_element_by(element_page['type'], driver, element_page['value'])

    def get_element_by_from_device(self, element_page, device, driver):
        if device['platformName'] == "WEB":
            return ManagementFile().get_element_by(element_page['type'], driver, element_page['value'])
        else:
            return ManagementFileAndroid().get_by_android(element_page['type'], driver, element_page['value'])

    def get_value_element_form_device(self, element, device):
        if device['platformName'] == "WEB":
            if element.get_attribute("value") is not None and element.tag_name == "input":
                return element.get_attribute('value')
            else:
                return element.text
        else:
                return element.text
    def get_value_attribute_element_form_device(self, element, device, value, flag):
        if device['platformName'] == "WEB":
            if flag:
                value_attribute = element.value_of_css_property(value)
                if 'color' in value:
                    return Color.from_string(value_attribute).hex.lower()
                else:
                    return value_attribute.lower()
            else:
                return element.get_attribute(value)
        elif device['platformName'] == "ANDROID":
            try:
                return element.get_attribute(value)
            except Exception as e:
                print(e)
                assert False, f'framework does not support for attribute {value}'
        else:
            assert False, f'Framework does not support for {device["platformName"]}'

    def create_random_user(self, locale):
        if locale:
            faker = Faker(locale)
        else:
            faker = Faker('en_US')
        logger.info(f'faker.unique.first_name() == {faker.unique.first_name()}')
        user = generate_user(faker.unique.first_name(), faker.unique.last_name(), faker.job(), faker.address(),
                             faker.phone_number(), faker.city(),
                             faker.state(), faker.postcode(), faker.domain_name(), faker.prefix(), faker.suffix())
        return user

    def verify_elements_below_attributes(self, page, row, platform_name, dict_save_value, driver, device, wait):
        arr_element = page['elements']
        arr_element = list(filter(
            lambda element: element['id'] == row[0], arr_element
        ))
        logger.info(f'Verifying for {row[0]} have value {row[1]} and status {row[2]}')
        value = row[1]
        helper = row[3]
        if value is None: value = ''
        if dict_save_value:
            if 'USER.' in value:
                value = self.get_value_from_user_random(value, dict_save_value)
            else:
                value = dict_save_value.get(value, value)
        element_yaml = self.get_element(page, arr_element[0]['id'] + " with text " + value, platform_name,
                                        dict_save_value)
        if row[2] and element_yaml:
            if value != '' and helper is None:
                logger.info(f'Verified for {row[0]} have value {row[1]} and status {row[2]}')
                self.verify_value_in_element(element_yaml, value, device, driver)
            else:
                logger.info(f'Verified for {row[0]} have value {row[1]} and status {row[2]}')
                self.wait_element_for_status(element_yaml, row[2], driver, device, wait)
        else:
            logger.error(f'table must be contains both field name and status')
            assert False, f'table must be contains both field name {row[0]} and status {row[2]}'
        self.verify_value_with_helpers(value, helper, element_yaml, device, driver)

    def get_value_from_user_random(self, value, dict_save_value):
        arr_user = value.split('USER.')
        list_user = dict_save_value['USER.']
        value = management_user.get_user(list_user, arr_user[1])
        return value
    def verify_value_in_element(self, element_page, expect, device, driver):
        element = self.get_element_by_from_device(element_page, device, driver)
        value = self.get_value_element_form_device(element, device)
        assert value == expect, f'value of the element not equal to values expected {expect}'

    def verify_value_with_helpers(self, expected, helper, element_page, device, driver):
        if helper in ['BACKGROUND-COLOR', 'COLOR', 'FONT_FAMILY', 'FONT_SIZE', 'FONT_WEIGHT', 'FONT_HEIGHT', 'TEXT_ALIGN'] and expected and device['platformName'] != 'WEB':
            assert False, f'framework only check {helper} for WEB env, not support for native app'
        if helper and expected:
            element = self.get_element_by_from_device(element_page, device, driver)
            if helper == 'REGEX':
                value_element = self.get_value_element_form_device(element, device)
                check_match_pattern(expected, value_element, 'value of element not match with pattern')
            elif helper == 'STARTS_WITH':
                value_element = self.get_value_element_form_device(element, device)
                assert value_element.startswith(expected), f'value of element is {expected} not start with {expected}'
            elif helper == 'ENDS_WITH':
                value_element = self.get_value_element_form_device(element, device)
                assert value_element.endswith(expected), f'value of element is {expected} not ends with {expected}'
            elif helper == 'CONTAINS':
                value_element = self.get_value_element_form_device(element, device)
                assert expected in value_element , f'value of element is {value_element} not contains {expected}'
            elif helper == 'BACKGROUND-COLOR':
                bg_color = self.get_value_attribute_element_form_device(element, device,'background-color', True)
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
        """Highlights (blinks) a Selenium Webdriver element"""
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
                assert True
                print(e)
    def save_coordinates_from_element(self, element_page, driver, key, dict_save_value, wait, device):
        try:
            # locator = ManagementFile().get_locator(element_page, device['platformName'])
            logger.info(f"save text for element {element_page['value']} with key is {key}")
            WebDriverWait(driver, wait).until(
                ec.presence_of_element_located(self.get_locator_for_wait_from_device(element_page, device)))
            element = self.get_element_by_from_device(element_page, device, driver)
            location = element.location
            dict_save_value["KEY." + key] = location
            return dict_save_value
        except Exception as e:
            logger.error(f"Can not save text for element {element_page['value']} with key is {key}")
            assert False, "Can not save text for element " + element_page['value']


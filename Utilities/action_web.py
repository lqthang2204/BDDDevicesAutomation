import glob
import json
import os
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from yaml import SafeLoader
from pyshadow.main import Shadow
from project_runner import logger, project_folder

class ManagementFile:
    def get_dict_path_yaml(self):
        file_path = os.path.join(project_folder, "resources", "pages", "*", "*.yaml")
        # print("file path =======================", file_path)
        dict_yaml = {}
        files = glob.glob(file_path, recursive=True)
        # print("glob = ", files)
        for file in files:
            # print("loop file ", file)
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        # dict_yaml_path = dict(dict_yaml)      # no needed
        return dict_yaml

    def read_yaml_file(self, path, dict_yaml, page_name, platform_name, dict_page_element):
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

    def execute_action(self, page, action_id, driver, wait, table, dict_save_value, platform_name):
        dict_action = page['actions']
        dict_action = list(filter(
            lambda action: action['id'] == action_id, dict_action
        ))
        type_action = None
        value = None
        if dict_action:
            obj_action = dict_action[0]
            arr_list_action = obj_action['actionElements']
            for action_elements in arr_list_action:
                if table is not None:
                    for row in table:
                        if action_elements['element']['id'] == row["Field"]:
                            value = row["Value"]
                            if dict_save_value:
                                value = dict_save_value.get(value, value)
                            break
                element_page = action_elements['element']
                if self.check_field_exist(action_elements, 'inputType'):
                    type_action = action_elements['inputType']
                locator = self.get_locator_from_action(element_page, platform_name)
                element = self.get_element_by(locator['type'], driver, locator['value'])
                if self.check_field_exist(action_elements, "condition") and self.check_field_exist(action_elements, "timeout"):
                    try:
                        if action_elements['condition'] == "ENABLED":
                            WebDriverWait(driver, action_elements['timeout']).until(
                                ec.element_to_be_clickable(element))
                        elif action_elements['condition'] == "NOT_ENABLED":
                            WebDriverWait(driver, action_elements['timeout']).until_not(
                                ec.element_to_be_clickable(element))
                        elif action_elements['condition'] == "DISPLAYED":
                            WebDriverWait(driver, action_elements['timeout']).until(
                                ec.presence_of_element_located(element))
                        elif action_elements['condition'] == "NOT_DISPLAYED":
                            WebDriverWait(driver, action_elements['timeout']).until(
                                ec.presence_of_element_located(element))
                        elif action_elements['condition'] == "EXISTED":
                            elements = self.get_list_element_by(locator['type'], driver, locator['value'])
                            WebDriverWait(driver, action_elements['timeout']()).until(
                                lambda driver: len(elements) > int(0))
                        elif action_elements['condition'] == "NOT_EXISTED":
                            elements = self.get_list_element_by(locator['type'], driver, locator['value'])
                            WebDriverWait(driver, action_elements['timeout']).until_not(
                                lambda driver: len(elements) > int(0))
                        elif action_elements['condition'] == "SELECTED":
                            WebDriverWait(driver, action_elements['timeout']).until(
                                ec.element_located_to_be_selected(element))
                        elif action_elements['condition'] == "NOT_SELECTED":
                            WebDriverWait(driver, action_elements['timeout']).until_not(
                                ec.element_located_to_be_selected(element))
                        else:
                            logger.error("Not support condition %s in framework", action_elements['condition'])
                            assert False, "Not support condition"
                        if type_action == "click":
                            if element.get_attribute("disabled") is None:
                                element.click()
                            else:
                                WebDriverWait(driver, action_elements['timeout']).until_not(
                                    ec.element_attribute_to_include(
                                        self.get_locator_for_wait(locator['type'], locator['value']), "disabled"))
                                element.click()
                        elif type_action == "text":
                            element.send_keys(value)
                    except Exception as e:
                        logger.info(f'can not execute action with element have value  {locator} in framework')
                        assert True, "can not execute action with element have value" + locator + "in framework"
                elif self.check_field_exist(action_elements, 'condition') and self.check_field_exist(action_elements, 'timeout') is False:
                    try:
                        self.process_execute_action(driver, wait, element, type_action, value, locator, action_elements)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator['value'])
                        assert False, "can not execute action " + type_action + " with element have value" + locator[
                            'value'] + "in framework"
                else:
                    try:
                        self.process_execute_action(driver, wait, element, type_action, value,
                                                    locator)
                    except Exception as e:
                        logger.error("can not execute action % with element have value  %s in framework", type_action,
                                     locator.value)
                        assert False, "can not execute action " + type_action + " with element have value" + locator.value + "in framework"
        else:
            logger.error(f'Not Found Action {action_id} in page yaml')
            assert False, "Not Found Action " + action_id + " in page yaml"

    def get_element_by(self, type, driver, value):
        logger.info(f'Get element by {type} with value is {value}')
        if type.__eq__("ID"):
            element = driver.find_element(By.ID, value)
        elif type.__eq__("NAME"):
            element = driver.find_element(By.NAME, value)
        elif type.__eq__("XPATH"):
            element = driver.find_element(By.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            element = driver.find_element(By.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            element = driver.find_element(By.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            element = driver.find_element(By.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            element = driver.find_element(By.CSS_SELECTOR, value)
        else:
            logger.error(f'Can not get  element by {type} with value is {value}')
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type, driver, value):
        logger.info(f'Get list element by {type} with value is {value}')
        if type.__eq__("ID"):
            elements = driver.find_elements(By.ID, value)
        elif type.__eq__("NAME"):
            elements = driver.find_elements(By.NAME, value)
        elif type.__eq__("XPATH"):
            elements = driver.find_elements(By.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            elements = driver.find_elements(By.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            elements = driver.find_elements(By.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            elements = driver.find_elements(By.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            elements = driver.find_elements(By.CSS_SELECTOR, value)
        else:
            logger.error(f'Can not get  element by {type} with value is {value}')
            raise Exception("Not support type in framework")
        return elements

    def get_locator_for_wait(self, type, value):
        logger.info(f'get locator for wait with type {type} with value is {value}')
        if type.__eq__("ID"):
            locator = (By.ID, value)
        elif type.__eq__("NAME"):
            locator = (By.NAME, value)
        elif type.__eq__("XPATH"):
            locator = (By.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            locator = (By.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            locator = (By.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            locator = (By.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            locator = (By.CSS_SELECTOR, value)
        else:
            logger.error(f'Not support type {type} in framework')
            raise Exception(f'Not support type {type} in framework')
        return locator

    def get_locator(self, element_page, device):
        arr_locator = element_page.get_list_locator()
        for locator in arr_locator:
            if locator.get_device().__eq__(device):
                return locator

    def get_locator_from_action(self, element_page, device):
        # print(element_page)
        for locator in element_page['locators']:
            if locator['device'].__eq__(device):
                return locator

    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def process_execute_action(self, driver, wait, element, type_action, value, locator, action_elements):
        logger.info(f'execute action  {type_action} with element have value {locator}')
        if type_action == 'click':
            WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(
                        self.get_locator_for_wait(locator[type], locator['value']), "disabled"))
                element.click()
        elif type_action == "text":
            WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
            element.send_keys(value)
        else:
            self.wait_for_action(action_elements, wait, driver, element, locator)

    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except:
            return False

    def wait_for_action(self, action_elements, wait, driver, element, locator):
        locator_from_wait = self.get_locator_for_wait(locator['type'], locator['value'])
        try:
            if action_elements['condition'] == "ENABLED":
                WebDriverWait(driver, wait).until(
                    ec.element_to_be_clickable(locator_from_wait))
            elif action_elements['condition'] == "NOT_ENABLED":
                WebDriverWait(driver, action_elements['timeout']).until_not(
                    ec.element_to_be_clickable(locator_from_wait))
            elif action_elements['condition'] == "DISPLAYED":
                WebDriverWait(driver, wait).until(
                    ec.presence_of_element_located(locator_from_wait))
            elif action_elements['condition'] == "NOT_DISPLAYED":
                WebDriverWait(driver, wait).until(
                    ec.presence_of_element_located(locator_from_wait))
            elif action_elements['condition'] == "EXISTED":
                elements = self.get_list_element_by(locator['type'], driver, locator['value'])
                WebDriverWait(driver, wait).until(
                    lambda driver: len(elements) > int(0))
            elif action_elements['condition'] == "NOT_EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, wait).until_not(
                    lambda driver: len(elements) > int(0))
            elif action_elements['condition'] == "SELECTED":
                WebDriverWait(driver, wait).until(
                    ec.element_located_to_be_selected(locator_from_wait))
            elif action_elements['condition'] == "NOT_SELECTED":
                WebDriverWait(driver, wait).until_not(
                    ec.element_located_to_be_selected(locator_from_wait))
            else:
                logger.error(f'Not support condition {action_elements} in framework')
                assert False, "Not support condition"
        except Exception as e:
            logger.info(f'can not execute action with element have value  {locator} in framework')
            assert False, "can not execute action with element have value" + locator['value'] + "in framework"
    def get_shadow_element(self, type, driver, value, wait, is_highlight):
        logger.info(f'finding shadow element {value}')
        shadow = Shadow(driver)
        shadow.set_explicit_wait(wait, 1)
        if type == 'CSS':
            element = shadow.find_element(value, False)
            if is_highlight == 'true':
                shadow.highlight(element, color='red', time_in_mili_seconds=0.2)
            return element
        elif type == 'XPATH':
            element = shadow.find_element_by_xpath(value, False)
            if is_highlight == 'true':
                shadow.highlight(element, color='red', time_in_mili_seconds=0.2)
            return element
        else:
            logger.error(f'the type of shadow element must be CSS type, type is {type}')
            assert False, f'the type of shadow element must be CSS type'
    def action_with_shadow_element(self, element_page, action, driver, value, wait, dict_save_value, is_highlight):
        element = self.get_shadow_element(element_page['type'], driver, element_page['value'], wait, is_highlight)
        logger.info(f'execute {action} with element have is {element_page["value"]}')
        if action.__eq__("click"):
            element.click()
        elif action.__eq__("type"):
            if dict_save_value:
                value = dict_save_value.get(value, value)
            element.send_keys(value)
        elif action.__eq__("clear"):
            element.clear()
        elif action.__eq__("wait"):
            WebDriverWait(driver, wait).until(
                ec.presence_of_element_located(element))
        else:
            logger.error("Can not execute %s with element have is %s", action)
            assert False, "Not support action in framework"
    def action_mouse(self,action, element_page_from, element_page_to, context):
        element_from = self.get_element_by(element_page_from['type'], context.driver, element_page_from['value'])
        logger.info(f'execute {action} with element have is {element_page_from["value"]}')
        if action.__eq__('drag-and-drop'):
            action = ActionChains(context.driver)
            element_to = self.get_element_by(element_page_to['type'], context.driver, element_page_to['value'])
            logger.info(f'execute {action} with element have is {element_page_to["value"]}')
            action.drag_and_drop(element_from, element_to).perform()
        else:
            logger.error("Can not execute %s with element have is %s", action)
            assert False, "Not support action in framework"
    def handle_popup(self,driver, status):
        alert = driver.switch_to.alert
        if status == 'accept':
            alert.accept()
        elif status == 'dismiss':
            alert.dismiss()
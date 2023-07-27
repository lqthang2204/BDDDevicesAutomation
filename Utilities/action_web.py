import os
import glob
import yaml
from yaml import SafeLoader
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import logging

class ManagementFile:
    def get_dict_path_yaml(self):
        file_path = os.path.dirname(os.path.dirname(__file__)) + "/resources/pages/*/*.yaml"
        print("file path =======================", file_path)
        dict_yaml = {}
        files = glob.glob(file_path, recursive=True)
        print("glob = ", files)
        for file in files:
            print("lopp file ", file)
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        # dict_yaml_path = dict(dict_yaml)
        return dict_yaml

    def read_yaml_file(self, path, dict_yaml, page_name):
        if page_name in dict_yaml.keys():
            obj_page = dict_yaml[page_name]
            return obj_page
        else:
            obj_page = Page()
            dict_yaml[page_name] = obj_page
            with open(path, encoding='utf-8') as page:
                python_dict = yaml.load(page.read(), Loader=SafeLoader)
                json_result = json.dumps(python_dict)
                json_object = json.loads(json_result)
                dict_yaml[page_name] = json_object
            return json_object
    def execute_action(self, page, action_id, driver, wait, table, dict_save_value, platformName):
        dict_action = page['actions']
        if dict_action:
            dict_action = list(filter(
                lambda action: action['id'] == action_id, dict_action
            ))
            arr_list_action = dict_action[0]['actionElements']
            for action_elements in arr_list_action:
                if table is not None:
                    for row in table:
                        if action_elements['element']['id'] == row["Field"]:
                            value = row["Value"]
                            if dict_save_value:
                                value = dict_save_value.get(value, value)
                        break
                element_page = action_elements['element']['locators']
                element_page = list(filter(
                    lambda loc: loc['device'] == platformName, element_page
                ))
                type_action = None
                if 'inputType' in action_elements:
                    type_action = action_elements['inputType']
                locator = self.get_locator_from_action(element_page, platformName)
                element = self.get_element_by(locator['type'], driver, locator['value'])
                if self.check_field_exist(action_elements,'condition') and self.check_field_exist(action_elements, 'timeout'):
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
                            WebDriverWait(driver, action_elements['timeout']).until(
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
                            logging.error("Not support condition %s in framework", action_elements['condition']())
                            assert False, "Not support condition"
                        if type_action.__eq__("click"):
                            if element.get_attribute("disabled") is None:
                                element.click()
                            else:
                                WebDriverWait(driver, action_elements['timeout']).until_not(
                                    ec.element_attribute_to_include(
                                        self.get_locator_for_wait(locator['type'], locator['value']), "disabled"))
                                element.click()
                        elif type_action.__eq__("text"):
                            element.send_keys(value)
                    except Exception as e:
                        logging.info(f'can not execute action with element have value  {locator} in framework')
                        assert True, "can not execute action with element have value" + locator + "in framework"
                elif self.check_field_exist(action_elements,'condition') and self.check_field_exist(action_elements,'timeout') is False:
                    try:
                        self.process_execute_action(driver, wait, element, type_action, value,
                                                    locator)
                    except Exception as e:
                        logging.error("can not execute action % with element have value  %s in framework", type_action,
                                      locator['value'])
                        assert False, "can not execute action " + type_action + " with element have value" + locator['value'] + "in framework"
                else:
                    try:
                        self.process_execute_action(driver, wait, element, type_action, value,
                                                    locator)
                    except Exception as e:
                        logging.error("can not execute action % with element have value  %s in framework", type_action,
                                      locator['value'])
                        assert False, "can not execute action " + type_action + " with element have value" + locator['value'] + "in framework"
        else:
            logging.error(f'Not Found Action {action_id} in page yaml')
            assert False, "Not Found Action " + action_id + " in page yaml"

    def get_element_by(self, type, driver, value):
        logging.info("Get element by %s with value is %s", type, value);
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
            logging.error("Can not get  element by %s with value is %s", type, value);
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type, driver, value):
        logging.info("Get list element by %s with value is %s", type, value);
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
            logging.error("Can not get  element by %s with value is %s", type, value);
            raise Exception("Not support type in framework")
        return elements

    def get_locator_for_wait(self, type, value):
        logging.info("get locator for wait with type %s and value is %s ", type, value)
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
            logging.error("Not support type %s in framework", type)
            raise Exception("Not support type in framework", type)
        return locator

    def get_locator(self, element_page, device):
        arr_locator = element_page['locators']
        for locator in arr_locator:
            if locator['device'].__eq__(device):
                return locator

    def get_locator_from_action(self, element_page, device):
        # print(element_page)
        for locator in element_page:
            if locator['device'].__eq__(device):
                return locator

    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def process_execute_action(self, driver, wait, element, type_action, value, locator):
        WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
        logging.info("execute action  %s with element have value %s", type_action, locator['value']);
        if type_action.__eq__("click"):
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(
                        self.get_locator_for_wait(locator['type'], locator['value']), "disabled"))
                element.click()
        elif type_action.__eq__("text"):
            element.send_keys(value)
    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except:
            return False

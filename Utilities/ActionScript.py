import os
import glob
import yaml
from yaml import SafeLoader
import json
from ManagementElements.Page import Page
from ManagementElements.Elements import Elements
from ManagementElements.Locator import Locator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from ManagementElements.ActionTest import ActionTest
from ManagementElements.ActionElements import ActionElements


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
            list_element = list()
            with open(path) as page:
                python_dict = yaml.load(page.read(), Loader=SafeLoader)
                json_result = json.dumps(python_dict)
                json_object = json.loads(json_result)
                print("json =", json_object)
                arr_element = json_object["elements"]
                for element in arr_element:
                    obj_element = Elements()
                    obj_element.set_id(element["id"])
                    obj_element.set_description(element["description"])
                    arr_locator = element["locators"]
                    list_locator = list()
                    for locator in arr_locator:
                        obj_locator = Locator()
                        obj_locator.set_device(locator["device"])
                        obj_locator.set_type(locator["type"])
                        obj_locator.set_value(locator["value"])
                        list_locator.append(obj_locator)
                    obj_element.set_list_locator(list_locator)
                    list_element.append(obj_element)
                obj_page.set_list_element(list_element)
                dict_action = {}
                arr_action = self.check_att_is_exist(json_object, "actions")
                if arr_action is not None:
                    for action in arr_action:
                        obj_action = ActionTest()
                        obj_action.set_id(action["id"])
                        obj_action.set_description(action["description"])
                        arr_action_elements = action["actionElements"]
                        list_action_element = list()
                        for action_elements in arr_action_elements:
                            obj_action_elements = ActionElements()
                            obj_locator = action_elements["element"]
                            arr_locator = obj_locator["locators"]
                            obj_action_elements.set_id(obj_locator["id"])
                            list_locator = list()
                            for locator_action in arr_locator:
                                obj_locator = Locator()
                                obj_locator.set_device(locator_action["device"])
                                obj_locator.set_type(locator_action["type"])
                                obj_locator.set_value(locator_action["value"])
                                list_locator.append(obj_locator)
                            obj_action_elements.set_element(list_locator)
                            obj_action_elements.set_condition(self.check_att_is_exist(action_elements, "condition"))
                            obj_action_elements.set_timeout(self.check_att_is_exist(action_elements, "timeout"))
                            obj_action_elements.set_inputType(self.check_att_is_exist(action_elements, "inputType"))
                            obj_action_elements.set_info_type(self.check_att_is_exist(action_elements, "infoType"))
                            list_action_element.append(obj_action_elements)
                            obj_action.set_list_action(list_action_element)
                        dict_action[action["id"]] = obj_action
                obj_page.set_dict_action(dict_action)
                dict_yaml[page_name] = obj_page
            return obj_page

    def get_element(self, page, element):
        arr_element = page.list_element
        for element_yaml in arr_element:
            if element_yaml.id.__eq__(element):
                return element_yaml

    def execute_action(self, page, action_id, driver, wait, table, dict_save_value):
        dict_action = page.get_dict_action()
        if dict_action[action_id] is not None:
            obj_action = dict_action[action_id]
            arr_list_action = obj_action.get_list_action()
            for action_elements in arr_list_action:
                if table is not None:
                    for row in table:
                        if action_elements.get_id() == row["Field"]:
                            if dict_save_value is not None and row["Value"] in dict_save_value.keys():
                               value = dict_save_value[row["Value"]]
                            else:
                                value = row["Value"]
                            break
                    element_page = action_elements.get_element()
                    type_action = action_elements.get_inputType()
                    locator = self.get_locator_from_action(element_page, "WEB")
                    element = self.get_element_by(locator.type, driver, locator.value)
                    if action_elements.get_condition() is not None and action_elements.get_timeout() is not None:
                        try:
                            if action_elements.get_condition() == "ENABLED":
                                WebDriverWait(driver, action_elements.get_timeout()).until(
                                    ec.element_to_be_clickable(element))
                            elif action_elements.get_condition() == "NOT_ENABLED":
                                WebDriverWait(driver, action_elements.get_timeout()).until_not(
                                    ec.element_to_be_clickable(element))
                            elif action_elements.get_condition() == "DISPLAYED":
                                WebDriverWait(driver, action_elements.get_timeout()).until(
                                    ec.presence_of_element_located(element))
                            elif action_elements.get_condition() == "NOT_DISPLAYED":
                                WebDriverWait(driver, action_elements.get_timeout()).until(
                                    ec.presence_of_element_located(element))
                            elif action_elements.get_condition() == "EXISTED":
                                elements = self.get_list_element_by(locator.type, driver, locator.value)
                                WebDriverWait(driver, action_elements.get_timeout()).until(
                                    lambda driver: len(elements) > int(0))
                            elif action_elements.get_condition() == "NOT_EXISTED":
                                elements = self.get_list_element_by(locator.type, driver, locator.value)
                                WebDriverWait(driver, action_elements.get_timeout()).until_not(
                                    lambda driver: len(elements) > int(0))
                            elif action_elements.get_condition() == "SELECTED":
                                WebDriverWait(driver, action_elements.get_timeout()).until(
                                    ec.element_located_to_be_selected(element))
                            elif action_elements.get_condition() == "NOT_SELECTED":
                                WebDriverWait(driver, action_elements.get_timeout()).until_not(
                                    ec.element_located_to_be_selected(element))
                            else:
                                assert False, "Not support condition"
                            if type_action.__eq__("click"):
                                if element.get_attribute("disabled") is None:
                                    element.click()
                                else:
                                    WebDriverWait(driver, action_elements.get_timeout).until_not(
                                        ec.element_attribute_to_include(
                                            self.get_locator_for_wait(locator.type, locator.value), "disabled"))
                                    element.click()
                            elif type.__eq__("text"):
                                element.send_keys(value)
                        except:
                            assert True, "due to have Condition and time out by pass step"
                    elif action_elements.get_condition() is not None and action_elements.get_timeout() is None:
                        try:
                            self.process_execute_action(driver, wait, element, type_action, value,
                                                        locator)
                        except:
                            assert False, "Failed at action step"
                    else:
                        try:
                            self.process_execute_action(driver, wait, element, type_action, value,
                                                        locator)
                        except:
                            assert False, "Failed at action step"
        else:
            assert False, "Not Found Action in page yaml"

    def action_page(self, element_page, action, driver, value, wait, dict_save_value):
        locator = self.get_locator(element_page, "WEB")
        element = self.get_element_by(locator.type, driver, locator.value)
        WebDriverWait(driver, wait).until(ec.all_of(
            ec.element_to_be_clickable(element)),
            ec.presence_of_element_located(element)
        )
        if action.__eq__("click"):
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(self.get_locator_for_wait(locator.type, locator.value), "disabled"))
                element.click()
        elif action.__eq__("type"):
            if len(dict_save_value) == int(0):
                element.send_keys(value)
            else:
                if dict_save_value[value] is not None:
                    value = dict_save_value[value]
                    element.send_keys(value)
                else:
                    assert False, "Not key in map save text"
        elif action.__eq__("clear"):
            element.clear()
        else:
            assert False, "Not support action in framework"
    def save_text_from_element(self, element_page, driver, key, dict_save_value, wait):
        locator = self.get_locator(element_page, "WEB")
        WebDriverWait(driver, wait).until(ec.presence_of_element_located(self.get_locator_for_wait(locator.type, locator.value)))
        element = self.get_element_by(locator.type, driver, locator.value)
        if element.get_attribute("value") is None:
            value = element.text
        else:
            value = element.get_attribute('value')
        dict_save_value["KEY."+key] = value
        return dict_save_value

    def get_element_by(self, type, driver, value):
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
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type, driver, value):
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
            raise Exception("Not support type in framework")
        return elements

    def get_locator_for_wait(self, type, value):
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
            raise Exception("Not support type in framework", type)
        return locator

    def get_locator(self, element_page, device):
        arr_locator = element_page.get_list_locator()
        for locator in arr_locator:
            if locator.get_device().__eq__(device):
                return locator
            break

    def get_locator_from_action(self, element_page, device):
        print(element_page)
        for locator in element_page:
            if locator.get_device().__eq__(device):
                return locator
            break

    def wait_element_for_status(self, element_page, status, driver, wait):
        locator = self.get_locator(element_page, "WEB")
        locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
        try:
            if status == "DISPLAYED":
                WebDriverWait(driver, wait).until(ec.presence_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, wait).until(ec.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, wait).until(ec.all_of(
                    ec.element_to_be_clickable(locator_from_wait)),
                    ec.presence_of_element_located(locator_from_wait))
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, wait).until_not(ec.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, wait).until(lambda driver: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, wait).until_not(lambda driver: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, wait).until(ec.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, wait).until_not(ec.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except TimeoutException as ex:
            assert False, "failed due to wait time out element"

    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def process_execute_action(self, driver, wait, element, type_action, value, locator):
        WebDriverWait(driver, wait).until(ec.element_to_be_clickable(element))
        if type_action.__eq__("click"):
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(
                        self.get_locator_for_wait(locator.type, locator.value), "disabled"))
                element.click()
        elif type_action.__eq__("text"):
            element.send_keys(value)
    # def __check_wait_element__(self,status, locator_from_wait):
    #     if status == "ENABLED":
    #         element = EC.presence_of_element_located(locator_from_wait)
    #         visibility = EC.visibility_of_element_located(locator_from_wait)
    #         if element
    #             try:
    #                 return True
    #             except:
    #                 return False
    #         else:
    #             return False

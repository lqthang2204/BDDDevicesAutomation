import os
import pathlib
import sys
import glob
from typing import Dict, Any, List
from pathlib import Path
import yaml
from yaml import SafeLoader
import json
from ManagementElements.Page import Page
from ManagementElements.Elements import Elements
from ManagementElements.Locator import Locator
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ManagementFile:
    def get_dict_path_yaml(self):
        # config_file_path = os.path.join(os.path.dirname(), 'config.ini')
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

    def read_yaml_file(path, dict_yaml, page_name):
        if page_name in dict_yaml.keys():
            obj_page = Page()
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
                dict_yaml[page_name] = obj_page
            return obj_page

    def get_element(self, page, element):
        arr_element = page.list_element
        for element_yaml in arr_element:
            if element_yaml.id.__eq__(element):
                return element_yaml

    def action_page(self, element_page, action, driver, value, wait):
        locator = self.get_locator(element_page, "WEB")
        element = self.get_element_by(locator.type, driver, locator.value)
        WebDriverWait(driver, wait).until(EC.all_of(
            EC.element_to_be_clickable(element)),
            EC.presence_of_element_located(element)
        )
        if action.__eq__("click"):
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(EC.element_attribute_to_include(self.get_locator_for_wait(locator.type, locator.value),"disabled"))
                element.click()
        elif action.__eq__("type"):
            element.send_keys(value)
        else:
            raise Exception("Not support action in framework")

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

    def wait_element_for_status(self, element_page, status, driver, wait):
        locator = self.get_locator(element_page, "WEB")
        locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)

        try:
            if status == "DISPLAYED":
                WebDriverWait(driver, wait).until(EC.presence_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, wait).until(EC.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, wait).until(EC.all_of(
                    EC.element_to_be_clickable(locator_from_wait)),
                    EC.presence_of_element_located(locator_from_wait)
                )
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, wait).until_not(EC.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, wait).until(lambda driver: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, wait).until_not(lambda driver: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, wait).until(EC.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, wait).until_not(EC.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except TimeoutException as ex:
            raise Exception("failed due to  timeout is ", wait)


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
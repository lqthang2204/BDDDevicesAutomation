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


class ManagementFile:
    def get_dict_path_yaml():
        file_path = os.getcwd().replace("Utilities","")+"\\resources\\pages\\*\\*.yaml"
        dict_yaml = {}
        files = glob.glob(file_path)
        for file in files:
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
                arr_element  = json_object["elements"]
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
            break
    def action_page(self, element_page, action, driver, value):
        locator = self.get_locator(element_page, "WEB")
        element = self.get_element_by(locator.type, driver, locator.value)
        if action.__eq__("click"):
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
    def get_locator(self, element_page,device):
        arr_locator = element_page.get_list_locator()
        for locator in arr_locator:
            if locator.get_device().__eq__(device):
                return locator
            break
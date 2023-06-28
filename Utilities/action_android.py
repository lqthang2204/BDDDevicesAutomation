import os
import glob
import yaml
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from yaml import SafeLoader
import json
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException, \
    NoSuchElementException, TimeoutException
from appium.webdriver.appium_service import AppiumService


class ManagementFileAndroid:

    def get_element(self, page, element):
        arr_element = page.list_element
        for element_yaml in arr_element:
            if element_yaml.id.__eq__(element):
                return element_yaml


    def action_page(self, element_page, action, driver, value, wait, dict_save_value, device):
        locator = self.get_locator(element_page, device.get_platform_name())
        element = self.get_by_android(locator.type, driver, locator.value)
        if action.__eq__("click"):
                element.click()
        elif action.__eq__("type"):
            if len(dict_save_value) == int(0):
                element.click()
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
        element = self.get_element(locator.type, driver, locator.value)
        if element.get_attribute("value") is None:
            value = element.text
        else:
            value = element.get_attribute('value')
        dict_save_value["KEY."+key] = value
        return dict_save_value

    def get_by_android(self,type, driver, value):
        if type.__eq__("ID"):
            element = driver.find_element(AppiumBy.ID, value)
        elif type.__eq__("NAME"):
            element = driver.find_element(AppiumBy.NAME, value)
        elif type.__eq__("XPATH"):
            element = driver.find_element(AppiumBy.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            element = driver.find_element(AppiumBy.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            element = driver.find_element(AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            element = driver.find_element(AppiumBy.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            element = driver.find_element(AppiumBy.CSS_SELECTOR, value)
        else:
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type, driver, value):
        if type.__eq__("ID"):
            elements = driver.find_elements(AppiumBy.ID, value)
        elif type.__eq__("NAME"):
            elements = driver.find_elements(AppiumBy.NAME, value)
        elif type.__eq__("XPATH"):
            elements = driver.find_elements(AppiumBy.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            elements = driver.find_elements(AppiumBy.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            elements = driver.find_elements(AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            elements = driver.find_elements(AppiumBy.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            elements = driver.find_elements(AppiumBy.CSS_SELECTOR, value)
        else:
            raise Exception("Not support type in framework")
        return elements

    def get_locator(self, element_page, device):
        arr_locator = element_page.get_list_locator()
        for locator in arr_locator:
            if locator.get_device().__eq__(device):
                return locator

    def get_locator_from_action(self, element_page, device):
        print(element_page)
        for locator in element_page:
            if locator.get_device().__eq__(device):
                return locator
            break

    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def wait_element_for_status(self, element_page, status, driver, device):
        locator = self.get_locator(element_page, device.get_platform_name())
        locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
        try:
            if status == "DISPLAYED":
                print("locator = ", locator_from_wait)
                WebDriverWait(driver, device.get_wait()).until(expected_conditions.presence_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, device.get_wait()).until(expected_conditions.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, device.get_wait()).until(expected_conditions.all_of(
                    expected_conditions.element_to_be_clickable(locator_from_wait)),
                    expected_conditions.presence_of_element_located(locator_from_wait))
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, device.get_wait()).until_not(expected_conditions.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, device.get_wait()).until(lambda driver: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, device.get_wait()).until_not(lambda driver: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, device.get_wait()).until(expected_conditions.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, device.get_wait()).until_not(expected_conditions.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except TimeoutException as ex:
            assert False, "failed due to wait time out element"


    def get_locator_for_wait(self, type, value):
        if type.__eq__("ID"):
            locator = (AppiumBy.ID, value)
        elif type.__eq__("NAME"):
            locator = (AppiumBy.NAME, value)
        elif type.__eq__("XPATH"):
            locator = (AppiumBy.XPATH, value)
        elif type.__eq__("LINK TEXT"):
            locator = (AppiumBy.LINK_TEXT, value)
        elif type.__eq__("PARTIAL LINK TEXT"):
            locator = (AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type.__eq__("CLASS NAME"):
            locator = (AppiumBy.CLASS_NAME, value)
        elif type.__eq__("CSS"):
            locator = (AppiumBy.CSS_SELECTOR, value)
        elif type.__eq__("ACCESSIBILITY_ID"):
            locator = (AppiumBy.ACCESSIBILITY_ID, value)
        else:
            raise Exception("Not support type in framework", type)
        return locator


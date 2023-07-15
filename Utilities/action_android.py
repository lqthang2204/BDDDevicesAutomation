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
import logging


class ManagementFileAndroid:

    def get_element(self, page, element):
        arr_element = page.list_element
        for element_yaml in arr_element:
            if element_yaml.id.__eq__(element):
                return element_yaml

    def action_page(self, element_page, action, driver, value, dict_save_value, device):
        try:
            locator = self.get_locator(element_page, device.get_platform_name())
            locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
            logging.info("execute %s with element have is %s", action, locator.value)
            WebDriverWait(driver, device.get_wait()).until(
                expected_conditions.presence_of_element_located(locator_from_wait))
            element = self.get_by_android(locator.type, driver, locator.value)
            if action.__eq__("click"):
                WebDriverWait(driver, device.get_wait()).until(
                    expected_conditions.element_to_be_clickable(locator_from_wait))
                element.click()
            elif action.__eq__("type"):
                if not dict_save_value:
                    element.click()
                    element.send_keys(value)
                else:
                    value = dict_save_value.get(value, value)
                    element.send_keys(value)
            elif action.__eq__("clear"):
                element.clear()
            else:
                logging.error("Can not execute %s with element have is %s", action, locator.value)
                assert False, "Not support action in framework"
        except Exception as e:
            logging.error("Can not execute %s with element have is %s", action, locator.value)
            assert False, e

    def save_text_from_element(self, element_page, driver, key, dict_save_value, wait):
        locator = self.get_locator(element_page, "WEB")
        element = self.get_element(locator.type, driver, locator.value)
        if element.get_attribute("value") is None:
            value = element.text
        else:
            value = element.get_attribute('value')
        dict_save_value["KEY." + key] = value
        return dict_save_value

    def get_by_android(self, type_element, driver, value):
        logging.info("Get element by %s with value is %s", type_element, value);
        if type_element.__eq__("ID"):
            element = driver.find_element(AppiumBy.ID, value)
        elif type_element.__eq__("NAME"):
            element = driver.find_element(AppiumBy.NAME, value)
        elif type_element.__eq__("XPATH"):
            element = driver.find_element(AppiumBy.XPATH, value)
        elif type_element.__eq__("LINK TEXT"):
            element = driver.find_element(AppiumBy.LINK_TEXT, value)
        elif type_element.__eq__("PARTIAL LINK TEXT"):
            element = driver.find_element(AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type_element.__eq__("CLASS NAME"):
            element = driver.find_element(AppiumBy.CLASS_NAME, value)
        elif type_element.__eq__("CSS"):
            element = driver.find_element(AppiumBy.CSS_SELECTOR, value)
        elif type_element.__eq__("ACCESSIBILITY_ID"):
            element = driver.find_elemen(AppiumBy.ACCESSIBILITY_ID, value)
        else:
            logging.error("Can not get  element by %s with value is %s", type_element, value);
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type_element, driver, value):
        logging.info("Get list element by %s with value is %s", type_element, value);
        if type_element.__eq__("ID"):
            elements = driver.find_elements(AppiumBy.ID, value)
        elif type_element.__eq__("NAME"):
            elements = driver.find_elements(AppiumBy.NAME, value)
        elif type_element.__eq__("XPATH"):
            elements = driver.find_elements(AppiumBy.XPATH, value)
        elif type_element.__eq__("LINK TEXT"):
            elements = driver.find_elements(AppiumBy.LINK_TEXT, value)
        elif type_element.__eq__("PARTIAL LINK TEXT"):
            elements = driver.find_elements(AppiumBy.PARTIAL_LINK_TEXT, value)
        elif type_element.__eq__("CLASS NAME"):
            elements = driver.find_elements(AppiumBy.CLASS_NAME, value)
        elif type_element.__eq__("CSS"):
            elements = driver.find_elements(AppiumBy.CSS_SELECTOR, value)
        elif type_element.__eq__("ACCESSIBILITY_ID"):
            elements = driver.find_elemen(AppiumBy.ACCESSIBILITY_ID, value)
        else:
            logging.error("Can not get  element by %s with value is %s", type_element, value);
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

    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def wait_element_for_status(self, element_page, status, driver, device):
        locator = self.get_locator(element_page, device.get_platform_name())
        locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
        logging.info("wait element have value  %s with the status %s", locator.value, status);
        try:
            if status == "DISPLAYED":
                print("locator = ", locator_from_wait)
                WebDriverWait(driver, device.get_wait()).until(
                    expected_conditions.presence_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, device.get_wait()).until(
                    expected_conditions.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, device.get_wait()).until(expected_conditions.all_of(
                    expected_conditions.element_to_be_clickable(locator_from_wait)),
                    expected_conditions.presence_of_element_located(locator_from_wait))
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, device.get_wait()).until_not(
                    expected_conditions.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, device.get_wait()).until(lambda driver: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by(locator.type, driver, locator.value)
                WebDriverWait(driver, device.get_wait()).until_not(lambda driver: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, device.get_wait()).until(
                    expected_conditions.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, device.get_wait()).until_not(
                    expected_conditions.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except TimeoutException as ex:
            logging.error("The status %s is not currently.", status);
            assert False, "failed due to wait time out element"

    def get_locator_for_wait(self, type, value):
        logging.info("get locator for wait with type %s and value is %s ", type, value)
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
            logging.error("Not support type %s in framework", type)
            raise Exception("Not support type in framework", type)
        return locator

    def execute_action_android(self, page, action_id, driver, wait, table, dict_save_value):
        value = None
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
                locator = self.get_locator_from_action(element_page, "ANDROID")
                # element = self.get_by_android(locator.type, driver, locator.value)
                locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
                if action_elements.get_condition() is not None and action_elements.get_timeout() is not None:
                    try:
                        if action_elements.get_condition() == "ENABLED":
                            WebDriverWait(driver, action_elements.get_timeout()).until(
                                expected_conditions.element_to_be_clickable(locator_from_wait))
                        elif action_elements.get_condition() == "NOT_ENABLED":
                            WebDriverWait(driver, action_elements.get_timeout()).until_not(
                                expected_conditions.element_to_be_clickable(locator_from_wait))
                        elif action_elements.get_condition() == "DISPLAYED":
                            WebDriverWait(driver, action_elements.get_timeout()).until(
                                expected_conditions.presence_of_element_located(locator_from_wait))
                        elif action_elements.get_condition() == "NOT_DISPLAYED":
                            WebDriverWait(driver, action_elements.get_timeout()).until(
                                expected_conditions.presence_of_element_located(locator_from_wait))
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
                                expected_conditions.element_located_to_be_selected(locator_from_wait))
                        elif action_elements.get_condition() == "NOT_SELECTED":
                            WebDriverWait(driver, action_elements.get_timeout()).until_not(
                                expected_conditions.element_located_to_be_selected(locator_from_wait))
                        else:
                            logging.error("Not support condition %s in framework", action_elements.get_condition())
                            assert False, "Not support condition"
                        if type_action.__eq__("click"):
                            WebDriverWait(driver, action_elements.get_timeout()).until(
                                expected_conditions.element_to_be_clickable(locator_from_wait))
                            element = self.get_by_android(locator.type, driver, locator.value)
                            element.click()
                        elif type_action.__eq__("text"):
                            WebDriverWait(driver, action_elements.get_timeout()).until(
                                expected_conditions.presence_of_element_located(locator_from_wait))
                            element = self.get_by_android(locator.type, driver, locator.value)
                            element.send_keys(value)
                    except Exception as e:
                        logging.info("can not execute action with element have value  %s in framework", locator.value)
                        assert True, "can not execute action with element have value" + locator.value + "in framework"
                elif action_elements.get_condition() is not None and action_elements.get_timeout() is None:
                    try:
                        self.process_execute_action(driver, wait, type_action, value, locator_from_wait, locator)
                    except Exception as e:
                        logging.error("can not execute action % with element have value  %s in framework", type_action,
                                      locator.value)
                        assert False, "can not execute action " + type_action + " with element have value" + locator.value + "in framework"
                else:
                    try:
                        self.process_execute_action(driver, wait, type_action, value, locator_from_wait, locator)
                    except Exception as e:
                        logging.error("can not execute action % with element have value  %s in framework", type_action,
                                      locator.value)
                        assert False, "can not execute action " + type_action + " with element have value" + locator.value + "in framework"
        else:
            logging.error("Not Found Action %s in page yaml", action_id)
            assert False, "Not Found Action " + action_id + " in page yaml"

    def process_execute_action(self, driver, wait, type_action, value, locator_from_wait, locator):
        WebDriverWait(driver, wait).until(expected_conditions.presence_of_element_located(locator_from_wait))
        element = self.get_by_android(locator.type, driver, locator.value)
        logging.info("execute action  %s with element have value %s", type_action, locator.value);
        if type_action is not None:
            WebDriverWait(driver, wait).until(expected_conditions.element_to_be_clickable(element))
            if type_action.__eq__("click"):
                element.click()
            elif type_action.__eq__("text"):
                element.send_keys(value)
        # else:
        #     locator_from_wait = self.get_locator_for_wait(locator.type, locator.value)
        #     WebDriverWait(driver, wait).until(expected_conditions.presence_of_element_located(locator_from_wait))

    def save_text_from_element_android(self, element_page, driver, key, dict_save_value, wait):
        try:
            locator = self.get_locator(element_page, "ANDROID")
            logging.info("save text for element  %s with key is %s", locator.value, key);
            WebDriverWait(driver, wait).until(
                expected_conditions.presence_of_element_located(self.get_locator_for_wait(locator.type, locator.value)))
            element = self.get_by_android(locator.type, driver, locator.value)
            if element.get_attribute("content-desc") is None:
                value = element.text
            else:
                value = element.get_attribute('content-desc')
            dict_save_value["KEY." + key] = value
            return dict_save_value
        except Exception as e:
            logging.error("Can not save text for element  %s with key is %s", locator.value, key);
            assert False, "Can not save text for element " + locator.value

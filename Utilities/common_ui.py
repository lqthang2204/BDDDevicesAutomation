import logging

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from Utilities.action_android import ManagementFileAndroid
from Utilities.action_web import ManagementFile


class common_device:
    def check_att_is_exist(self, obj_action_elements, key):
        if obj_action_elements.get(key) is None:
            return None
        else:
            return obj_action_elements.get(key)

    def action_page(self, element_page, action, driver, value, wait, dict_save_value, device):
        locator = ManagementFile().get_locator(element_page, device.get_platform_name())
        element = self.get_element_by_from_device(locator, device, driver)
        logging.info("execute %s with element have is %s", action, locator.value)
        WebDriverWait(driver, wait).until(ec.all_of(
            ec.element_to_be_clickable(element)),
            ec.presence_of_element_located(element)
        )
        if action.__eq__("click"):
            self.click_action(element, wait, locator, device, driver)
        elif action.__eq__("type"):
            if dict_save_value:
                value = dict_save_value.get(value, value)
            element.send_keys(value)
        elif action.__eq__("clear"):
            element.clear()
        else:
            logging.error("Can not execute %s with element have is %s", action, locator.value)
            assert False, "Not support action in framework"

    def click_action(self, element, wait, locator, device, driver):
        if device.get_platform_name() == "WEB":
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(ManagementFile().get_locator_for_wait(locator.type, locator.value),
                                                    "disabled"))
                element.click()
        else:
            locator_from_wait = ManagementFileAndroid().get_locator_for_wait(locator.type, locator.value)
            WebDriverWait(driver, wait).until(
                ec.element_to_be_clickable(locator_from_wait))
            element.click()

    def wait_element_for_status(self, element_page, status, driver, device):
        locator = ManagementFile().get_locator(element_page, device.get_platform_name())
        locator_from_wait = self.get_locator_for_wait_from_device(locator, device)
        logging.info("wait element have value  %s with the status %s", locator.value, status);
        try:
            if status == "DISPLAYED":
                WebDriverWait(driver, device.get_wait()).until(ec.presence_of_element_located(locator_from_wait))
            elif status == "NOT_DISPLAYED":
                WebDriverWait(driver, device.get_wait()).until(ec.invisibility_of_element_located(locator_from_wait))
            elif status == "ENABLED":
                WebDriverWait(driver, device.get_wait()).until(ec.all_of(
                    ec.element_to_be_clickable(locator_from_wait)),
                    ec.presence_of_element_located(locator_from_wait))
            elif status == "NOT_ENABLED":
                WebDriverWait(driver, device.get_wait()).until_not(ec.element_to_be_clickable(locator_from_wait))
            elif status == "EXISTED":
                elements = self.get_list_element_by_from_device(locator, device, driver)
                WebDriverWait(driver, device.get_wait()).until(lambda ele: len(elements) > int(0))
            elif status == "NOT_EXISTED":
                elements = self.get_list_element_by_from_device(locator, device, driver)
                WebDriverWait(driver, device.get_wait()).until_not(lambda ele: len(elements) > int(0))
            elif status == "SELECTED":
                WebDriverWait(driver, device.get_wait()).until(ec.element_located_to_be_selected(locator_from_wait))
            elif status == "NOT_SELECTED":
                WebDriverWait(driver, device.get_wait()).until_not(ec.element_located_to_be_selected(locator_from_wait))
            else:
                raise Exception("Not support status ", status)
        except Exception as e:
            logging.error("The status %s is not currently.", status);
            assert False, e

    def get_element(self, page, element, platform_name, dict_save_value):
        text = ""
        if "with text" in element:
            arr_value = element.split("with text")
            # remove blank in array
            arr_value = [i.lstrip() for i in arr_value]
            element = arr_value[0].strip()
            # remove double quote
            text = arr_value[1]
            if dict_save_value:
                text = dict_save_value.get(text, text)
        arr_element = page.list_element
        for element_yaml in arr_element:
            if element_yaml.id.__eq__(element):
                arr_locator = element_yaml.list_locator
                arr_locator = list(filter(
                    lambda loc: loc.device == platform_name,
                    arr_locator
                ))
                if len(arr_locator) == 1:
                    arr_locator[0].value = arr_locator[0].value.replace("{text}", text)
                    return element_yaml

    def verify_elements_with_status(self, page, table, platform_name, dict_save_value, driver, device):
        arr_element = page.list_element
        if table is not None:
            for row in table:
                for element_yaml in arr_element:
                    if element_yaml.id.__eq__(row["Field"]):
                        logging.info("Verifying for %s have value %s and status %s", row["Field"], row["Value"],
                                     row["Status"])
                        value = row["Value"]
                        if dict_save_value:
                            value = dict_save_value.get(value, value)
                        element_yaml = self.get_element(page, element_yaml.id + " with text " + value, platform_name,
                                                        dict_save_value)
                        self.wait_element_for_status(element_yaml, row["Status"], driver, device)
                        logging.info("Verified for %s have value %s and status %s", row["Field"], row["Value"],
                                     row["Value"])
        else:
            logging.error("user must set data table for elements")
            assert False, "can not execute verify status for elements"

    def save_text_from_element(self, element_page, driver, key, dict_save_value, wait, device):
        try:
            locator = ManagementFile().get_locator(element_page, device.get_platform_name())
            logging.info("save text for element  %s with key is %s", locator.value, key);
            WebDriverWait(driver, wait).until(
                ec.presence_of_element_located(self.get_locator_for_wait_from_device(locator, device)))
            element = self.get_element_by_from_device(locator, device, driver)
            value = self.get_value_element_form_device(element, device)
            dict_save_value["KEY." + key] = value
            return dict_save_value
        except Exception as e:
            logging.error("Can not save text for element  %s with key is %s", locator.value, key);
            assert False, "Can not save text for element " + locator.value

    def get_locator_for_wait_from_device(self, locator, device):
        if device.get_platform_name() == "WEB":
            return ManagementFile().get_locator_for_wait(locator.type, locator.value)
        else:
            return ManagementFileAndroid().get_locator_for_wait(locator.type, locator.value)

    def get_list_element_by_from_device(self, locator, device, driver):
        if device.get_platform_name() == "WEB":
            return ManagementFile().get_list_element_by(locator.type, driver, locator.value)
        else:
            return ManagementFileAndroid().get_list_element_by(locator.type, driver, locator.value)

    def get_element_by_from_device(self, locator, device, driver):
        if device.get_platform_name() == "WEB":
            return ManagementFile().get_element_by(locator.type, driver, locator.value)
        else:
            return ManagementFileAndroid().get_by_android(locator.type, driver, locator.value)

    def get_value_element_form_device(self, element, device):
        if device.get_platform_name() == "WEB":
            if element.get_attribute("value") is not None and element.tag_name == "input":
                return element.get_attribute('value')
            else:
                return element.text
        else:
            if element.get_attribute("content-desc") is None:
                return element.text
            else:
                return element.get_attribute('content-desc')

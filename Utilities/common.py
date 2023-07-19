import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
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
        element = ManagementFile().get_element_by(locator.type, driver, locator.value)
        logging.info("execute %s with element have is %s", action, locator.value)
        WebDriverWait(driver, wait).until(ec.all_of(
            ec.element_to_be_clickable(element)),
            ec.presence_of_element_located(element)
        )
        if action.__eq__("click"):
            if element.get_attribute("disabled") is None:
                element.click()
            else:
                WebDriverWait(driver, wait).until_not(
                    ec.element_attribute_to_include(ManagementFile().get_locator_for_wait(locator.type, locator.value), "disabled"))
                element.click()
        elif action.__eq__("type"):
            if dict_save_value:
                value = dict_save_value.get(value, value)
            element.send_keys(value)
        elif action.__eq__("clear"):
            element.clear()
        else:
            logging.error("Can not execute %s with element have is %s", action, locator.value)
            assert False, "Not support action in framework"

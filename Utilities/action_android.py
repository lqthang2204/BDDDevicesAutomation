from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from project_runner import logger


class ManagementFileAndroid:
    def get_by_android(self, type_element, driver, value):
        logger.info(f'Get element by {type_element} with value is {value}')
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
            element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, value)
        elif type_element.__eq__("IOS_PREDICATE"):
            element = driver.find_element(AppiumBy.IOS_PREDICATE, value)
        elif type_element.__eq__("IOS_CLASS_CHAIN"):
            if value[:1] == '/':
                value = value[1:]
            element = driver.find_element(AppiumBy.IOS_CLASS_CHAIN, value)
        else:
            logger.error(f'Can not get  element by {type_element} with value is {value}')
            raise Exception("Not support type in framework")
        return element

    def get_list_element_by(self, type_element, driver, value):
        logger.info(f'Get list element by by {type_element} with value is {value}')
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
        elif type_element.__eq__("IOS_PREDICATE"):
            elements = driver.find_elemen(AppiumBy.IOS_PREDICATE, value)
        elif type_element.__eq__("IOS_CLASS_CHAIN"):
            if value[:1] == '/':
                value = value[1:]
            elements = driver.find_elemen(AppiumBy.IOS_CLASS_CHAIN, value)
        else:
            logger.error(f'Can not get  element by {type_element} with value is {value}')
            raise Exception("Not support type in framework")
        return elements

    def get_locator(self, element_page, device):
        arr_locator = element_page.get_list_locator()
        for locator in arr_locator:
            if locator.get_device().__eq__(device):
                return locator

    def get_locator_from_action(self, element_page, device):
        for locator in element_page['locators']:
            if locator['device'].__eq__(device):
                return locator

    def check_att_is_exist(self, obj_action_elements, key, default=None):
        return obj_action_elements.get(key, default)

    def get_locator_for_wait(self, type, value):
        logger.info(f'get locator for wait with type by {type} with value is {value}')
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
        elif type.__eq__("IOS_PREDICATE"):
            locator = (AppiumBy.IOS_PREDICATE, value)
        elif type.__eq__("IOS_CLASS_CHAIN"):
            if value[:1] == '/':
                value = value[1:]
            locator = (AppiumBy.IOS_CLASS_CHAIN, value)
        else:
            logger.error("Not support type %s in framework", type)
            raise Exception("Not support type in framework", type)
        return locator

    def check_field_exist(self, dict, key):
        try:
            if dict[key]:
                return True
        except:
            return False

    def action_mouse_mobile(self,action, element_page_from, element_page_to, context):
        element_from = self.get_by_android(element_page_from['type'], context.driver, element_page_from['value'])
        logger.info(f'execute {action} with element have is {element_page_from["value"]}')
        if action.__eq__('drag-and-drop'):
            touch_action = TouchAction(context.driver)
            element_to = self.get_by_android(element_page_to['type'], context.driver, element_page_to['value'])
            touch_action.tap(element_from).perform()
            touch_action.long_press(element_from).move_to(element_to).release().perform()
            logger.info(f'execute {action} with element have is {element_page_to["value"]}')
        else:
            logger.error("Can not execute %s with element have is %s", action)
            assert False, "Not support action in framework"
    def scroll_from_to_element(self, element_page_from, element_page_to, driver, wait):
        element_from_wait = self.get_locator_for_wait(element_page_from['type'], element_page_from['value'])
        element_to_wait = self.get_locator_for_wait(element_page_to['type'], element_page_from['value'])
        WebDriverWait(driver, wait).until(ec.presence_of_element_located(element_from_wait))
        WebDriverWait(driver, wait).until(ec.presence_of_element_located(element_to_wait))
        touch_action = TouchAction(driver)
        element_from = self.get_by_android(element_page_from['type'],driver, element_page_to['value'])
        element_to = self.get_by_android(element_page_to['type'], driver, element_page_to['value'])
        driver.findElementByAndroidUIAutomator
        # logger.info(f'execute {action} with element have is {element_page_to["value"]}')

    def scroll_mobile(self, action, element_destination, driver):
        element = self.get_locator_for_wait(element_destination['type'], element_destination['value'])
        logger.info(f'get element have is value is {element_destination["value"]}')
        logger.info(f'starting scroll to element {element_destination["value"]}')
        self.scroll(driver, action, element)
    def scroll(self, driver, action, element):
        sleep(1)
        flag = False
        window_size = driver.get_window_size()
        if action.__eq__('down'):
            start_y = window_size["height"] * 0.6
            end_y = window_size["height"] * 0.30
            start_x = window_size["width"] / 2
            for each in range(1, 3):
                driver.swipe(start_x, start_y, start_x, end_y, 2000)
                try:
                    WebDriverWait(driver, 10).until(ec.presence_of_element_located(element))
                    flag = True
                    break
                except:
                    assert True, f'Not found element {element} when scroll down, try again!'
        elif action.__eq__('up'):
            start_y = window_size["height"] * 0.30
            end_y = window_size["height"] * 0.60
            start_x = window_size["width"] / 2
            for each in range(1, 3):
                driver.swipe(start_x, start_y, start_x, end_y, 2000)
                try:
                    WebDriverWait(driver, 10).until(ec.presence_of_element_located(element))
                    flag = True
                    break
                except:
                    assert True, f'Not found element {element} when scroll down, try again!'
        elif action.__eq__('left'):
            print('left')
        elif action.__eq__('right'):
            print('right')
        else:
            assert False, "can not execute scroll to element with action " + action + " in framework"
        assert flag, f'not found element when scroll'
    def close_application(self, driver):
        if driver.session_id:
            try:
                driver.quit()
                # driver.terminateApp('com.apple.Health')
            except Exception as e:
                logger.error('can not close application ', e)
                assert False, 'can not close application'





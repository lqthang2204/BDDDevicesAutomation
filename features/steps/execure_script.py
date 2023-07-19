import configparser
from behave import *
from selenium import webdriver
from Utilities.action_web import ManagementFile
from ManagementElements.Page import Page
from ManagementElements.Elements import Elements
from ManagementElements.Locator import Locator
from Utilities.action_android import ManagementFileAndroid
from Utilities.common import common_device

dict_yaml = {}
dict_page = {}
read_yaml: str
page_present = Page
element_page = Elements
locator = Locator
dict_save_value = {}


@step(u'I navigate to url have index {index}')
def launchBrowser(context, index):
    array_url = context.url.split(",")
    context.driver.get(array_url[int(index) - 1].strip())


@step(u'I open application')
def step_impl(context):
    print("run application")


@step(u'I change the page spec to {page}')
def change_page(context, page):
    path_file = context.dict_yaml[page + ".yaml"]
    page = ManagementFile().read_yaml_file(path_file + "/" + page + ".yaml", dict_page, page)
    context.page_present = page
    return context.page_present


@step(u'I click element {element}')
def click_action(context, element):
    context.element_page = ManagementFile().get_element(context.page_present, element,
                                                        context.device.get_platform_name(), context.dict_save_value)
    if context.device.get_platform_name() == "WEB":
        common_device().action_page(context.element_page, "click", context.driver, "", context.wait,
                                    context.dict_save_value, context.device)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().action_page(context.element_page, "click", context.driver, "",
                                            context.dict_save_value, context.device)



@step(u'I type "{text}" into element {element}')
def type_action(context, text, element):
    context.element_page = ManagementFile().get_element(context.page_present, element,
                                                        context.device.get_platform_name(), context.dict_save_value)
    if context.device.get_platform_name() == "WEB":
        common_device().action_page(context.element_page, "type", context.driver, text, context.wait,
                                    context.dict_save_value, context.device)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().action_page(context.element_page, "type", context.driver, text, context.dict_save_value,
                                            context.device)


@step(u'I wait for element {element} to be {status}')
def wait_element(context, element, status):
    context.element_page = ManagementFile().get_element(context.page_present, element,
                                                        context.device.get_platform_name(), context.dict_save_value)
    if context.device.get_platform_name() == "WEB":
        ManagementFile().wait_element_for_status(context.element_page, status, context.driver, context.wait)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().wait_element_for_status(context.element_page, status, context.driver, context.device)


@step(u'I wait for elements with below status')
def step_impl(context):
    if context.device.get_platform_name() == "WEB":
        context.element_page = ManagementFile().get_element_from_data_table(context.page_present, context.table, context.device.get_platform_name(), context.dict_save_value, context.driver, context.wait)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().wait_element_for_status(context.element_page, context.table, context.driver, context.device)
@step(u'I perform {action} action')
def step_impl(context, action):
    if context.device.get_platform_name() == "WEB":
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, None, None)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.device.get_wait(), None, None)


@step(u'I perform {action} action with override values')
def step_impl(context, action):
    if context.device.get_platform_name() == "WEB":
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, context.table,
                                        context.dict_save_value)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.device.get_wait(), context.table,
                                                       context.dict_save_value)


@step(u'I clear text from element {element}')
def step_impl(context, element):
    context.element_page = ManagementFile().get_element(context.page_present, element,
                                                        context.device.get_platform_name(), context.dict_save_value)
    if context.device.get_platform_name() == "WEB":
        common_device().action_page(context.element_page, "clear", context.driver, "", context.wait,
                                    context.dict_save_value, context.device)
    elif context.device.get_platform_name() == "ANDROID":
        ManagementFileAndroid().action_page(context.element_page, "clear", context.driver, "", context.dict_save_value,
                                            context.device)


@step(u'I save text for element {element} with key "{key}"')
def step_impl(context, element, key):
    context.element_page = ManagementFile().get_element(context.page_present, element,
                                                        context.device.get_platform_name(), context.dict_save_value)
    if context.device.get_platform_name() == "WEB":
        context.dict_save_value = ManagementFile().save_text_from_element(context.element_page, context.driver, key,
                                                                          context.dict_save_value, context.wait)
    elif context.device.get_platform_name() == "ANDROID":
        context.dict_save_value = ManagementFileAndroid().save_text_from_element_android(context.element_page,
                                                                                         context.driver, key,
                                                                                         context.dict_save_value,
                                                                                         context.wait)
        # print(context.dict_save_value)
    return context.dict_save_value


@step(u'I wait 5 seconds')
def step_impl(context):
    print("wait")

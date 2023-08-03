from behave import *

from Utilities.action_android import ManagementFileAndroid
from Utilities.action_web import ManagementFile
from Utilities.common_ui import common_device



@step(u'I navigate to url {name}')
def launchBrowser(context, name):
    context.driver.get(context.url[name])

@step(u'I change the page spec to {page}')
def change_page(context, page):
    path_file = context.dict_yaml[page + ".yaml"]
    page = ManagementFile().read_yaml_file(path_file + "/" + page + ".yaml", context.dict_yaml, page, context.device['platformName'],  context.dict_page_element)
    context.page_present = page
    return context.page_present


@step(u'I click element {element}')
def click_action(context, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "click", context.driver, "", context.wait,
                                context.dict_save_value, context.device)


@step(u'I type "{text}" into element {element}')
def type_action(context, text, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "type", context.driver, text, context.wait,
                                context.dict_save_value, context.device)


@step(u'I wait for element {element} to be {status}')
def wait_element(context, element, status):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().wait_element_for_status(context.element_page, status, context.driver, context.device, context.wait)


@step(u'I wait for elements with below status')
def step_impl(context):
    context.element_page = common_device().verify_elements_with_status(context.page_present, context.table,
                                                                       context.device['platformName'],
                                                                       context.dict_save_value, context.driver,
                                                                       context.device, context.wait)


@step(u'I perform {action} action')
def step_impl(context, action):
    if context.device['platformName'] == "WEB":
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, None, None)
    elif context.device['platformName'] == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.device.get_wait(), None, None)


@step(u'I perform {action} action with override values')
def step_impl(context, action):
    if context.device['platformName'] == "WEB":
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, context.table,
                                        context.dict_save_value)
    elif context.device['platformName'] == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.device.get_wait(), context.table,
                                                       context.dict_save_value)


@step(u'I clear text from element {element}')
def step_impl(context, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "clear", context.driver, "", context.wait,
                                context.dict_save_value, context.device)


@step(u'I save text for element {element} with key "{key}"')
def step_impl(context, element, key):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    context.dict_save_value = common_device().save_text_from_element(context.element_page, context.driver, key,
                                                                     context.dict_save_value, context.wait,
                                                                     context.device)
    return context.dict_save_value

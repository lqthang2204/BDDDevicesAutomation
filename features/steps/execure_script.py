import os

from behave import *
from libraries.misc_operations import sanitize_datatable
from Utilities.action_android import ManagementFileAndroid
from Utilities.action_web import ManagementFile
from Utilities.common_ui import common_device
from libraries.faker import management_user


@step(u'I navigate to url {name}')
def launchBrowser(context, name):
    context.driver.get(context.url[name])


@step(u'I change the page spec to {page}')
def change_page(context, page):
    path_file = context.dict_yaml[page + ".yaml"]
    page = ManagementFile().read_yaml_file(os.path.join(path_file, page+'.yaml'), context.dict_yaml, page, context.device['platformName'], context.dict_page_element)
    context.page_present = page
    return context.page_present


@step(u'I click element {element}')
def click_action(context, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "click", context.driver, "", context.wait,
                                context.dict_save_value, context.device, context)


@step(u'I type "{text}" into element {element}')
def type_action(context, text, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "type", context.driver, text, context.wait,
                                context.dict_save_value, context.device, context)


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
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, None, None, context.device['platformName'])
    elif context.device['platformName'] == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.wait, None, None, context.device['platformName'])


@step(u'I perform {action} action with override values')
def step_impl(context, action):
    if context.device['platformName'] == "WEB":
        ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, context.table,
                                        context.dict_save_value, context.device['platformName'])
    elif context.device['platformName'] == "ANDROID":
        ManagementFileAndroid().execute_action_android(context.page_present, action, context.driver,
                                                       context.device.get_wait(), context.table,
                                                       context.dict_save_value, context.device['platformName'])


@step(u'I clear text from element {element}')
def step_impl(context, element):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    common_device().action_page(context.element_page, "clear", context.driver, "", context.wait,
                                context.dict_save_value, context.device, context)


@step(u'I save text for element {element} with key "{key}"')
def step_impl(context, element, key):
    context.element_page = common_device().get_element(context.page_present, element,
                                                       context.device['platformName'], context.dict_save_value)
    context.dict_save_value = common_device().save_text_from_element(context.element_page, context.driver, key,
                                                                     context.dict_save_value, context.wait,
                                                                     context.device)
    return context.dict_save_value


@step(u'I create a random user')
def step_impl(context):
    user = common_device().create_random_user(None)
    management_user.save_user_to_dict(context.dict_save_value, user)

@step(u'I verify that following elements with below attributes')
def step_impl(context):
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            context.element_page = common_device().verify_elements_below_attributes(context.page_present, row,
                                                                               context.device['platformName'],
                                                                               context.dict_save_value, context.driver,
                                                                               context.device, context.wait)
@step(u'I {action} shadow element {element}')
def step_impl(context, action, element):
    if context.device['platformName'] == "WEB":
        context.element_page = common_device().get_element(context.page_present, element,
                                                           context.device['platformName'], context.dict_save_value)
        value = ''
        if 'type' in action and 'into' in action:
            arr_value = action.split("\"")
            arr_value = [i.strip().lstrip() for i in arr_value]
            value = arr_value[1]
            action = arr_value[0]
        ManagementFile().action_with_shadow_element(context.element_page, action, context.driver, value, context.wait,
                                    context.dict_save_value, context)
    else:
        assert False, "only support action script with WEB ENVIRONMENT in framework"
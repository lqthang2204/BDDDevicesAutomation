import configparser
from behave import *
from selenium import webdriver
from Utilities.ActionScript import ManagementFile
from ManagementElements.Page import Page
from ManagementElements.Elements import Elements
from ManagementElements.Locator import Locator

dict_yaml = {}
dict_page = {}
read_yaml: str
page_present = Page
element_page = Elements
locator = Locator
dict_save_value = {}
@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    context.driver.maximize_window()
    context.driver.get(url)
    print("done")

@given(u'I change the page spec to {page}')
def change_page(context, page):
    path_file = context.dict_yaml[page+".yaml"]
    page = ManagementFile().read_yaml_file(path_file+"/"+page+".yaml", dict_page, page)
    context.page_present = page
    return context.page_present
@given(u'I click element {element}')
def click_action(context, element):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    ManagementFile().action_page(context.element_page, "click",context.driver,"", context.wait, context.dict_save_value)
@given(u'I type "{text}" into element {element}')
def type_action(context, text, element):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    ManagementFile().action_page(context.element_page, "type", context.driver, text, context.wait, context.dict_save_value)
@given(u'I wait for element {element} to be {status}')
def wait_element(context, element, status):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    ManagementFile().wait_element_for_status(context.element_page, status, context.driver, context.wait)

@given(u'I perform {action} action')
def step_impl(context,action):
    ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, None, None)

@given(u'I perform {action} action with override values')
def step_impl(context, action):
    ManagementFile().execute_action(context.page_present, action, context.driver, context.wait, context.table, context.dict_save_value)
@given(u'I clear text from element {element}')
def step_impl(context, element):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    ManagementFile().action_page(context.element_page, "clear", context.driver, "", context.wait)
@given(u'I save text for element {element} with key "{key}"')
def step_impl(context, element, key):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    context.dict_save_value = ManagementFile().save_text_from_element(context.element_page, context.driver, key, context.dict_save_value, context.wait)
    return context.dict_save_value
@given(u'I wait 5 seconds')
def step_impl(context):
    print("wait")












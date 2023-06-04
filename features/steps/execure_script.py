import configparser
from behave import *
from selenium import webdriver
from Utilities.ReadFileYaml import ManagementFile
from ManagementElements.Page import Page
from ManagementElements.Elements import Elements
from ManagementElements.Locator import Locator

dict_yaml = {}
dict_page = {}
read_yaml: str
page_present = Page
element_page = Elements
locator = Locator
@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    context.driver.maximize_window()
    context.driver.get(url)
    print("done")

@given(u'I change the page spec to {page}')
def change_page(context, page):
    dict_yaml = context.dict_yaml
    path_file = dict_yaml[page+".yaml"]
    page = ManagementFile.read_yaml_file(path_file+"\\"+page+".yaml", dict_page, page)
    context.page_present = page
    return context.page_present


@given(u'I click element {element}')
def click_action(context, element):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    try:
        ManagementFile().action_page(context.element_page, "click",context.driver,"", context.wait)
    except:
        raise Exception("Not found element ", element)
@given(u'I type "{text}" into element {element}')
def type_action(context, text, element):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    try:
        ManagementFile().action_page(context.element_page, "type", context.driver, text,context.wait)
    except:
        raise Exception("Not found element ", element)
@given(u'I wait for element {element} to be {status}')
def wait_element(context, element, status):
    context.element_page = ManagementFile().get_element(context.page_present, element)
    try:
        ManagementFile().wait_element_for_status(context.element_page, status, context.driver, context.wait)
    except:
        raise Exception("Not found element ", element)















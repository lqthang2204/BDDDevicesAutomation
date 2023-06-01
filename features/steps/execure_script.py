import configparser
from behave import *
from selenium import webdriver

@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    context.driver.maximize_window()
    context.driver.get(url)
    print("done")

@given(u'I change the page spec to {page}')
def change_page(context, page):
    print("page = "+ page)
    print(context.dict_yaml)






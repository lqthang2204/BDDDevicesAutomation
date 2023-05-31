import configparser
from behave import *
from selenium import webdriver
from common import common_test

@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    file = open("config.ini",'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read_file(file)
    if config.get("drivers_config","auto_download_driver") == 'True':
        context.driver = webdriver.Chrome(executable_path=config.get("drivers_config","driver_version"))
    else:
        context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.driver.get(url)
    print("done")

@given(u'I change the page spec to "{page}"')
def change_page(context, page):
    dict_yaml = common_test().get_dict_yaml()
    print("change page")
    print(dict_yaml)






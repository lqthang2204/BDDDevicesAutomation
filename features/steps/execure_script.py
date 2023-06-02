import configparser
from behave import *
from selenium import webdriver
from Utilities.ReadFileYaml import ManagementFile

dict_yaml = dict()
dict_page = dict()
read_yaml: str
@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    context.driver.maximize_window()
    context.driver.get(url)
    print("done")

@given(u'I change the page spec to {page}')
def change_page(context, page):
    dict_yaml = context.dict_yaml
    path_file = dict_yaml[page+".yaml"]
    ManagementFile.read_yaml_file(path_file+"\\"+page+".yaml")
    # print("after read yaml")
    # print(read_yaml)
    # ManagementFile.parse_yaml_file(read_yaml)







from behave import *
from selenium import webdriver
@given(u'I navigate to "{url}"')
def launchBrowser(context, url):
    context.driver = webdriver.Chrome()
    context.driver.get(url)
    print("done")

# @given(u'I change the page spec to {page}')
# def readFileYaml(context, page):
#     print("testtt   "+ page)





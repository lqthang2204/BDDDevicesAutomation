from Utilities.ReadFileYaml import ManagementFile
import configparser
from selenium import webdriver
import os
def before_all(context):
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
    file = open(config_file_path, 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read_file(file)
    if config.get("drivers_config", "auto_download_driver") == 'False':
        context.driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.dirname(__file__))+"\\"+config.get("drivers_config", "driver_version"))
    else:
        context.driver = webdriver.Chrome()
    print("----------------------Reading file config-----------------------------")
    context.dict_yaml = ManagementFile.get_dict_path_yaml()
    context.wait = config.get("drivers_config", "wait")
    context.time_page_load = config.get("drivers_config", "time_page_load")
# def before_scenario(context, scenario):
#     for tag in scenario.tags:
#         (platform, browser, browserVersion) = tag.split('_')
#
#         if browser == "Chrome":
#             # Initialize the browser with platform, browser, etc.
#             context.browser = webdriver.Chrome()
#         elif browser == "Firefox":
#             # Initialize the browser with platform, browser, etc.
#             context.browser = webdriver.Firefox()
from Utilities.ActionScript import ManagementFile
import configparser
from selenium import webdriver
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from Utilities.read_configuration import read_configuration
from Configuration.stage import stage
from Configuration.devices import devices
from Configuration.configuration_env import environment_config

# def before_all(context):
#     context.dict_save_value = {}
#     config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini')
#     file = open(config_file_path, 'r')
#     config = configparser.RawConfigParser(allow_no_value=True)
#     chrome_option = Options()
#     config.read_file(file)
#     if config.get("drivers_config", "is_headless") == 'true':
#         chrome_option.add_argument("--headless")
#     # chrome_option.add_argument("--no-sandbox")
#     # chrome_option.add_argument("--disable-dev-shm-usage")
#     chromedriver_autoinstaller.install()
#     if config.get("drivers_config", "auto_download_driver") == 'false':
#         context.driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.dirname(__file__))+"\\"+config.get("drivers_config", "driver_version"), options=chrome_option)
#     else:
#         context.driver = webdriver.Chrome(options=chrome_option)
#     print("----------------------Reading file config-----------------------------")
#     context.dict_yaml = ManagementFile().get_dict_path_yaml()
#     context.wait = config.get("drivers_config", "wait")
#     context.time_page_load = config.get("drivers_config", "time_page_load")

def before_all(context):
    context.dict_save_value = {}
    stage_config = stage()
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_env.ini')
    file = open(config_file_path, 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    chrome_option = Options()
    config.read_file(file)
    device = config.get("drivers_config", "device")
    stage_name = config.get("drivers_config", "stage")
    stage_config = read_configuration().read()
    print("stage config === ", stage_config)
    arr_config = stage_config.get_list_env()
    for config in arr_config:
        if stage_config.get_stage() == stage_name:

            if config == 'true':
                chrome_option.add_argument("--headless")
                # chrome_option.add_argument("--no-sandbox")
                # chrome_option.add_argument("--disable-dev-shm-usage")
            chromedriver_autoinstaller.install()
            if config.get("drivers_config", "auto_download_driver") == 'false':
                context.driver = webdriver.Chrome(
                    executable_path=os.path.dirname(os.path.dirname(__file__)) + "\\" + config.get("drivers_config",
                                                                                                   "driver_version"),
                    options=chrome_option)
            else:
                context.driver = webdriver.Chrome(options=chrome_option)
            print("----------------------Reading file config-----------------------------")
            context.dict_yaml = ManagementFile().get_dict_path_yaml()
            context.wait = config.get("drivers_config", "wait")
            context.time_page_load = config.get("drivers_config", "time_page_load")


    # listss = stage_config.get_list_env()
    # env_1 = listss[1]
    # arr_list = env_1.get_list_devices()
    # for arr in arr_list:
    #     print(arr.get_platform_name())


    # if config.get("drivers_config", "device") == 'web':
    #     chrome_option.add_argument("--headless")
    # # chrome_option.add_argument("--no-sandbox")
    # # chrome_option.add_argument("--disable-dev-shm-usage")
    # chromedriver_autoinstaller.install()
    # if config.get("drivers_config", "auto_download_driver") == 'false':
    #     context.driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.dirname(__file__))+"\\"+config.get("drivers_config", "driver_version"), options=chrome_option)
    # else:
    #     context.driver = webdriver.Chrome(options=chrome_option)
    # print("----------------------Reading file config-----------------------------")
    # context.dict_yaml = ManagementFile().get_dict_path_yaml()
    # context.wait = config.get("drivers_config", "wait")
    # context.time_page_load = config.get("drivers_config", "time_page_load")

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
def run_browser():






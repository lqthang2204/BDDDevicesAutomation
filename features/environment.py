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
    global wait, page_load_time
    context.dict_save_value = {}
    env = environment_config()
    stage_config = stage()
    device = devices()
    config_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config_env.ini')
    file = open(config_file_path, 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    chrome_option = Options()
    config.read_file(file)
    platform = config.get("drivers_config", "platform")
    stage_name = config.get("drivers_config", "stage")
    env = read_configuration().read()
    arr_stage = env.get_list_stage()
    for stage_config in arr_stage:
        print(stage_config.get_stage_name())
        if stage_config.get_stage_name() == stage_name:
            arr_device = stage_config.get_list_devices()
            for device in arr_device:
                if device.get_platform_name() == platform:
                    chrome_option = Options()
                    chromedriver_autoinstaller.install()
                    if device.get_is_headless():
                        chrome_option.add_argument("--headless")
                # chrome_option.add_argument("--no-sandbox")
                # chrome_option.add_argument("--disable-dev-shm-usage")
                    if device.get_auto_download_driver() is False:
                        context.driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.dirname(__file__)) + "\\" + device.get_driver_from_path(), options=chrome_option)
                    else:
                        context.driver = webdriver.Chrome(options=chrome_option)
                wait = device.get_wait()
                page_load_time = device .get_time_page_load()
                break
            print("----------------------Reading file config-----------------------------")
            context.dict_yaml = ManagementFile().get_dict_path_yaml()
            context.wait = wait
            context.time_page_load = page_load_time


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

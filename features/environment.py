from Utilities.action_web import ManagementFile
import configparser
from selenium import webdriver
import os
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from Utilities.read_configuration import read_configuration
from Configuration.stage import stage
from Configuration.devices import devices
from Configuration.configuration_env import environment_config
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
import datetime
import appium
import logging

def before_all(context):
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
    # arr_stage = env.get_list_stage()
    for stage_config in env:
        if stage_config['stage'] == stage_name:
            arr_device = stage_config['devices']
            for device in arr_device:
                if platform == "WEB" and device["platformName"] == platform:
                    launch_browser(context, device)
                    break
                elif platform == "ANDROID" and device["platformName"] == platform:
                    print("android")
                    launch_android(context, device, config)
                    context.wait = device["wait"]
                    context.time_page_load = device["time_page_load"]
                    break
                elif platform == "IOS" and device["platformName"] == platform:
                    print("IOS")
                    context.wait = device["wait"]
                    context.time_page_load = device["time_page_load"]
                    break
            context.url = stage_config['link']
            break
    context.dict_yaml = ManagementFile().get_dict_path_yaml()


def launch_browser(context, device):
    chrome_option = Options()
    chromedriver_autoinstaller.install()
    if device["is_headless"]:
        chrome_option.add_argument("--headless")
    if device["auto_download_driver"] is False:
        context.driver = webdriver.Chrome(
            executable_path=os.path.dirname(os.path.dirname(__file__)) + "\\" + device["driver_version"],
            options=chrome_option)
    else:
        context.driver = webdriver.Chrome(options=chrome_option)
    context.wait = device['wait']
    context.device = device
    context.time_page_load = device['time_page_load']
    context.driver.maximize_window()


def launch_android(context, device, config):
    # service = AppiumService()
    # service.start(args=['--address',config.get("drivers_config", "APPIUM_HOST"), '-P', str(config.get("drivers_config", "APPIUM_PORT"))], timeout_ms=20000)
    desired_caps = {
        'platformName': device['platformName'],
        'udid': device["udid"],
        'appPackage': device["appPackage"],
        "appActivity": device["appActivity"]
    }
    url = "http://" + config.get("drivers_config", "APPIUM_HOST") + ":" + str(
        config.get("drivers_config", "APPIUM_PORT")) + "/wd/hub"
    print(url)
    context.device = device
    context.wait = device["wait"]
    context.driver = appium.webdriver.Remote(url, desired_caps)


def after_step(context, step):
    if step.status == "failed":
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + "_" + str(current_time.month) + "_" + str(current_time.day) + "_" + str(
            current_time.microsecond)
        context.driver.get_screenshot_as_file(context.evidence_path + '/' + step.name + "_" + date_time + ".png")

def before_scenario(context, scenario):
    logging.info(f'Scenario Name started: {scenario.name}')

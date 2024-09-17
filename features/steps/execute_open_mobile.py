import configparser
import os

from selenium.common import SessionNotCreatedException

from project_runner import logger, project_folder
from appium import webdriver as appium_driver
import json
class manage_hook_mobile:
    def open_application(self, context, table):
        match context.device['platformName'].upper():
            case "ANDROID":
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    self.cross_browser_with_mobile(context, context.device, table)
                else:
                    options = self.create_android_driver(context, context.device, table)
                    self.launch_mobile(options, context)
                    context.wait = context.device['wait']
                    context.highlight = 'false'
            case "IOS":
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    self.cross_browser_with_mobile(context, context.device, table)
                else:
                    options = self.create_ios_driver(context, context.device, table)
                    self.launch_mobile(options, context)
                    context.wait = context.device['wait']
                    context.highlight = 'false'
            case _:
                assert False, f"platformName {context.device['platformName'].upper()} not support in framework"


    def cross_browser_with_mobile(self, context, device, table):
        config = self.read_config_remote()
        caps = self.get_data_config_mobile(context, device, table)
        caps['sauce:options'] = {}
        caps['sauce:options']['appiumVersion'] = '2.0.0'
        caps['sauce:options']['username'] = config.get("remote", "username")
        caps['sauce:options']['accessKey'] = config.get("remote", "accessKey")
        caps['sauce:options']['build'] = config.get("remote", "build")
        caps['sauce:options']['name'] = config.get("remote", "name")
        caps['sauce:options']['deviceOrientation'] = 'PORTRAIT'
        context.wait = device['wait']
        context.device = device
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()
        options.load_capabilities(caps)
        context.driver = appium_driver.Remote(config.get("remote", "url"), options=options)

    def get_data_config_mobile(self,context, device, table):
        config_file_path = os.path.join(context.root_path+"/configuration_env/", table[0][0]+".json")
        with open(config_file_path, 'r') as f:
            data = json.load(f)
        return data

    def read_config_remote(self):
        config_file_path = os.path.join(project_folder, 'remote_config.ini')
        file = open(config_file_path, 'r')
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_file(file)
        return config

    def launch_mobile(self, options, context):
        try:
            appium_url = self.check_att_exist(options, "appium_url")
            context.driver = appium_driver.Remote(appium_url, options = options, strict_ssl = False)
        except SessionNotCreatedException as ex:
            logger.error('Config file updated based on user provided command line arguments')
            print("not connect with remote saucelab, please check configuration again!")
            assert False, f'{ex.msg}'
    def check_att_exist(self, obj, key):
        if obj.get_capability(key) is None or obj.get_capability('appium:'+key) is None:
            return "127.0.0.1:4723"
        else:
            try:
                return obj.get_capability(key)
            except Exception as e:
                print("please check file input json" , e)
                assert False, e

    def create_ios_driver(self, context, device, table):
        desired_caps = self.get_data_config_mobile(context, device, table)
        from appium.options.ios import XCUITestOptions
        options = XCUITestOptions()
        options.load_capabilities(desired_caps)
        # Appium1 points to http://127.0.0.1:4723/wd/hub by default
        return options
    def create_android_driver(self, context, device, table):
        desired_caps = self.get_data_config_mobile(context, device, table)
        from appium.options.android import UiAutomator2Options
        options = UiAutomator2Options()
        options.load_capabilities(desired_caps)
        # Appium1 points to http://127.0.0.1:4723/wd/hub by default
        return options
    def navigate_url(self, context, name):
        try:
            if context.driver is None:
                context.driver.get(context.url[name])
            elif 'KEY.' in name and context.driver is not None:
                temp_url = context.dict_save_value[name]
                context.driver.get(temp_url)
            else:
                context.driver.get(context.url[name])
        except Exception as e:
            logger.error(f"An error occurred while navigating to URL: {str(e)}")



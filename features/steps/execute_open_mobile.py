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
                    self.launch_mobile(context, context.device, table, True)
                    context.wait = context.device['wait']
                    context.highlight = 'false'
            case "IOS":
                if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                    self.cross_browser_with_mobile(context, context.device, table)
                else:
                    self.launch_mobile(context, context.device, table, True)
                    context.wait = context.device['wait']
                    context.highlight = 'false'

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
        context.driver = appium_driver.Remote(config.get("remote", "url"), desired_capabilities=caps)

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

    def launch_mobile(self, context, device, table, flag):
        try:
            desired_caps = self.get_data_config_mobile(context, device, table)
            context.wait = device['wait']
            if flag:
                appium_url = self.check_att_exist(desired_caps, "appium_url")
                context.driver = appium_driver.Remote(appium_url, desired_capabilities=desired_caps, strict_ssl = False)
        except SessionNotCreatedException as ex:
            logger.error('Config file updated based on user provided command line arguments')
            print("not connect with remote saucelab, please check configuration again!")
            assert False, f'{ex.msg}'
    def check_att_exist(self, obj, key):
        if obj.get(key) is None:
            return "127.0.0.1:4723"
        else:
            return obj.get(key)

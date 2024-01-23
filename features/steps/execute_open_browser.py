import configparser
import datetime
import os
import json
from selenium import webdriver
from selenium.common import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as chrome_option
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.options import Options as firefox_option
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.safari.options import Options as safari_option
from selenium.webdriver.safari.service import Service as safari_service
from project_runner import logger, project_folder
from appium import webdriver as appium_driver
from execute_open_mobile import manage_hook_mobile as manage_remote
import json
class manage_hook_browser:
    def open_browser(self, context, table, name):
        try:
            if context.device['is_headless']:
                context.highlight = 'false'
            if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                self.cross_browser_with_web(context, context.device, table, name)
            else:
                 self.launch_browser(context, context.device, context.browser, table, name)
        except:
            logger.info('Framework only is support for chrome, firefox and safari..., script is supporting for browser')
            assert False, f"Framework only is support for chrome, firefox and safari..., script is supporting for browser"
    def launch_browser(self, context, device, browser, table, name):
        option = self.get_option_from_browser(browser, device, table)
        if device['auto_download_driver'] is False:
            self.get_driver_from_path(context, browser, device, option)
        else:
            match browser:
                case 'chrome':
                    context.driver = webdriver.Chrome(options=option)
                case 'firefox':
                    context.driver = webdriver.Firefox(options=option)
                case 'safari':
                    context.driver = webdriver.Safari()
                case fail:
                    logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
                    context.driver = webdriver.Chrome(options=option)
        context.wait = device['wait']
        context.time_page_load = device['time_page_load']
        if any("--window-size" in argument for argument in option.__getattribute__("arguments")) is False:
            context.driver.maximize_window()
        context.driver.get(context.url[name])
    def get_driver_from_path(context, browser, device, option):
        # //change due to update form selenium 4.10.0 , removed executable_path
        # https://github.com/SeleniumHQ/selenium/commit/9f5801c82fb3be3d5850707c46c3f8176e3ccd8e
        if browser == 'chrome':
            service = chrome_service(
                executable_path=project_folder + '\\' + device['driver_path'])
            context.driver = webdriver.Chrome(service=service, options=option)
        elif browser == 'firefox':
            service = firefox_service(
                executable_path=project_folder + '\\' + device['driver_path'])
            context.driver = webdriver.Firefox(service=service, options=option)
        elif browser == 'safari':
            service = safari_service(
                executable_path=project_folder + '\\' + device['driver_path'])
            context.driver = webdriver.Safari(service=service, options=option)
        else:
            logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
            service = chrome_service(
                executable_path=project_folder + '\\' + device['driver_version'])
            context.driver = webdriver.Chrome(service=service, options=option)

    def get_option_from_browser(self, browser, device, table):
        supported_browsers = {
            'chrome': chrome_option,
            'firefox': firefox_option,
            'safari': safari_option,
        }
        option = supported_browsers.get(browser.lower(), chrome_option)()
        if table:
            for rows in table:
                if rows[0] == 'argument':
                    option.add_argument(rows[1])
        if device['is_headless'] and browser.lower() in ['chrome', 'firefox']:
            option.add_argument('--headless')
        return option

    def cross_browser_with_web(self, context, device, table, name):
        config = manage_remote().read_config_remote()
        options = self.get_option_from_browser(config.get("remote", "browser"), device, table)
        options.browser_version = 'latest'
        options.platform_name = config.get("remote", "platform_name")
        sauce_options = {}
        sauce_options['username'] = config.get("remote", "username")
        sauce_options['accessKey'] = config.get("remote", "accessKey")
        sauce_options['build'] = config.get("remote", "build")
        sauce_options['name'] = config.get("remote", "name")
        options.set_capability('sauce:options', sauce_options)
        url = config.get("remote", "url")
        context.driver = webdriver.Remote(command_executor=url, options=options)
        context.wait = device['wait']
        context.device = device
        context.time_page_load = device['time_page_load']
        context.driver.maximize_window()
        context.driver.get(context.url[name])
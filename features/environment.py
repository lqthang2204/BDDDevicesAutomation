import configparser
import datetime
import os
from Utilities.action_web import ManagementFile
from Utilities.read_configuration import read_configuration
from project_runner import logger, project_folder
from sauceclient import SauceClient, SauceException
from steps.execute_open_mobile import manage_hook_mobile as manage_remote


def before_all(context):
    context.dict_save_value = {}
    context.driver = None
    context.root_path = project_folder
    config_file_path = os.path.join(context.root_path, 'config_env.ini')
    file = open(config_file_path, 'r')
    context.config_env = configparser.RawConfigParser(allow_no_value=True)
    context.config_env.read_file(file)
    context.platform = context.config_env.get("drivers_config", "platform").upper()
    context.highlight = context.config_env.get("drivers_config", "is_highlight").lower()
    context.project_folder = project_folder
    context.stage_name = context.config_env.get("drivers_config", "stage").upper()
    if context.config_env.has_option("drivers_config", "browser"):
        context.browser = context.config_env.get("drivers_config", "browser")
    else:
        context.browser = "chrome"
    context.env = read_configuration().read(context.stage_name)


def before_scenario(context, scenario):
    if context.platform != 'API':
        device = context.env['devices']
        context.device = list(filter(
            lambda device: device['platformName'] == context.platform, device
        ))
        if len(context.device) == 0:
            logger.error('Framework only is support for chrome, firefox and safari..., trying open with chrome')
        context.device = context.device[0]
        match context.device['platformName'].upper():
            case "WEB":
                # if context.device['is_headless']: context.highlight = 'false'
                # if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
                #     cross_browser_with_web(context, context.device)
                # else:
                #     launch_browser(context, context.device, context.browser)
                pass
            case "ANDROID":
                pass
            case "IOS":
                pass
            case fail:
                logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
                assert False, "Framework only is support for chrome, firefox and safari..., trying open with chrome"
        context.url = context.env['link']

    context.apiurls = context.env['apifacets']['link']
    context.endpoints = read_configuration().read_api_endpoints()
    logger.info(f'Scenario {scenario.name} started')
    context.dict_yaml = ManagementFile().get_dict_path_yaml()
    context.dict_page_element = {}


# def launch_browser(context, device, browser):
#     option = get_option_from_browser(browser, device)
#     if device['auto_download_driver'] is False:
#         get_driver_from_path(context, browser, device, option)
#     else:
#         match browser:
#             case 'chrome':
#                 context.driver = webdriver.Chrome(options=option)
#             case 'firefox':
#                 context.driver = webdriver.Firefox(options=option)
#             case 'safari':
#                 context.driver = webdriver.Safari()
#             case fail:
#                 logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
#                 context.driver = webdriver.Chrome(options=option)
#     context.wait = device['wait']
#     context.time_page_load = device['time_page_load']
#     context.driver.maximize_window()

def after_step(context, step):
    if step.status == 'failed':
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(
            current_time.microsecond)
        context.driver.get_screenshot_as_file(context.evidence_path + '/' + step.name + '_' + date_time + '.png')

def after_scenario(context, scenario):
    if context.driver:
        if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
            try:
                config = manage_remote().read_config_remote()
                sauce_client = SauceClient(config.get("remote", "username"), config.get("remote", "accessKey"))
                test_status = scenario.status == 'passed'
                sauce_client.jobs.update_job(context.driver.session_id, passed=test_status, name=scenario.name)
            except SauceException as e:
                print(e)
                print('can not update status for sauce lab')
                assert True
        context.driver.quit()
    logger.info(f'Scenario {scenario.name} Ended')
def after_all(context):
    if context.driver and context.platform == 'WEB':
        logger.info('Closing driver from After_ALL')
        context.driver.close()
        context.driver.quit()
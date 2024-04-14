import configparser
import datetime
import os
from Utilities.action_web import ManagementFile
from Utilities.read_configuration import read_configuration
from project_runner import logger, project_folder
from sauceclient import SauceClient, SauceException
from steps.execute_open_mobile import manage_hook_mobile as manage_remote
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry


def before_all(context):
    """
    Initializes the context with necessary values from the configuration file.
    """
    try:
        # Initialize dictionaries and variables in the context
        context.dict_save_value = {}
        context.driver = None
        context.root_path = project_folder

        # Read configuration file
        config_file_path = os.path.join(context.root_path, 'config_env.ini')
        file = open(config_file_path, 'r')
        context.config_env = configparser.RawConfigParser(allow_no_value=True)
        context.config_env.read_file(file)

        # Get platform and highlighting info from config
        context.platform = context.config_env.get("drivers_config", "platform").upper()
        context.highlight = context.config_env.get("drivers_config", "is_highlight").lower()

        # Set project folder and stage name
        context.project_folder = project_folder
        context.stage_name = context.config_env.get("drivers_config", "stage").upper()

        # Set browser based on config or default to chrome
        if context.config_env.has_option("drivers_config", "browser"):
            context.browser = context.config_env.get("drivers_config", "browser")
        else:
            context.browser = "chrome"

        # Read environment specific configuration
        context.env = read_configuration().read(context.stage_name)

    except Exception as e:
        # Log any errors that occur during initialization
        logger.error(str(e))
# def before_feature(context, feature):
    # rerun_failed_scenarios(context)

def before_scenario(context, scenario):
    """
    This function runs before a scenario is executed.
    It initializes the context based on the specific platform and environment settings.
    """
    try:
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
    except Exception as e:
        logger.error(str(e) + "with scenario " + scenario.name)


def before_feature(context, feature):
    """
    This function runs before a feature and patches scenarios with auto retry if configured to do so.

    Args:
        context (Context): The context object for the current execution.
        feature (Feature): The feature object being processed.
    """
    # Check if auto retry is configured
    if context.config_env.get("config_retry", "auto_retry").lower() == 'true':
        # Loop through all scenarios in the feature
        for scenario in feature.scenarios:
            # Check if the scenario should have auto retry
            if "final" in scenario.effective_tags:
                # Patch the scenario with auto retry settings
                patch_scenario_with_autoretry(scenario,
                                              max_attempts=int(context.config_env.get("config_retry", "max_attempts")))
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

import datetime

def after_step(context, step):
    """
    Takes a screenshot if the step fails and saves it in the evidence path provided in the context.

    Args:
        context (obj): The context object containing information about the test run.
        step (obj): The step object representing the current step being executed.
    """
    if step.status == 'failed' and hasattr(context, 'evidence_path'):
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(
            current_time.microsecond)
        context.driver.get_screenshot_as_file(context.evidence_path + '/' + step.name + '_' + date_time + '.png')


def after_scenario(context, scenario):
    """
    Takes appropriate actions after a scenario has run.

    Args:
        context (obj): The context object containing information about the test run.
        scenario (obj): The scenario object representing the current scenario that has been executed.
    """

    # Check if there is a driver present in the context
    if context.driver:
        if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
            try:
                # Read the configuration settings for remote execution
                config = manage_remote().read_config_remote()
                # Connect to the Sauce Labs client
                sauce_client = SauceClient(config.get("remote", "username"), config.get("remote", "accessKey"))
                # Determine the test status
                test_status = scenario.status == 'passed'
                # Update the job status on Sauce Labs
                sauce_client.jobs.update_job(context.driver.session_id, passed=test_status, name=scenario.name)
            except SauceException as e:
                # Handle exceptions if status update fails
                print(e)
                print('can not update status for sauce lab')
                assert True  # Assert to fail the scenario
        # Quit the driver
        context.driver.quit()
    # Log the ending of the scenario
    logger.info(f'Scenario {scenario.name} Ended')


# def after_feature(context, feature):
#     for scenario in feature.walk_scenarios():
#         if "final" in scenario.effective_tags:
#             patch_scenario_with_autoretry(scenario, max_attempts=60)


def after_all(context):
    # rerun_failed_scenarios(context)
    if context.driver and context.platform == 'WEB':
        logger.info('Closing driver from After_ALL')
        context.driver.close()



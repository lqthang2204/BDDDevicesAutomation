import configparser
import datetime
import os
from Utilities.action_web import ManagementFile
from Utilities.read_configuration import read_configuration
from project_runner import logger, project_folder
from sauceclient import SauceClient, SauceException
from steps.execute_open_mobile import manage_hook_mobile as manage_remote
from behavex_images import image_attachments
from behavex_images.image_attachments import AttachmentsCondition


def before_all(context):
    """
    Initializes the context with necessary values from the configuration file.
    """
    try:
        # image_attachments.set_attachments_condition(context, AttachmentsCondition.ONLY_ON_FAILURE)
        # Initialize dictionaries and variables in the context
        context.dict_save_value = {}
        context.driver = None
        context.root_path = project_folder
        context.driver = context.driver

        # Read configuration file
        config_file_path = os.path.join(context.root_path, 'config_env.ini')
        load_configuration(context, config_file_path)

        # Set platform-specific values
        context.platform = get_platform(context.config_env)
        context.highlight = get_highlight_flag(context.config_env)

        # Set stage and browser configurations
        context.stage_name = get_stage_name(context.config_env)
        context.browser = get_browser(context.config_env)

        # Load environment-specific configuration based on stage
        context.env = read_configuration().read(context.stage_name)

        # Log the successful initialization
        logger.info(
            f"Context successfully initialized for platform: {context.platform}, stage: {context.stage_name}, browser: {context.browser}")

    except Exception as e:
        # Log the exception and raise a RuntimeError to signal failure
        logger.error(f"Error initializing context: {str(e)}")
        raise RuntimeError(f"Failed to initialize context: {str(e)}")
# def before_feature(context, feature):
    # rerun_failed_scenarios(context)

def load_configuration(context, config_file_path):
    """
    Loads the configuration file and reads it into the context.

    Args:
        context (object): The context object to store the configuration.
        config_file_path (str): The path to the configuration file.
    """
    if not os.path.exists(config_file_path):
        logger.error(f"Configuration file not found: {config_file_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    logger.info(f"Loading configuration file: {config_file_path}")

    # Open the config file safely using 'with'
    with open(config_file_path, 'r') as file:
        context.config_env = configparser.RawConfigParser(allow_no_value=True)
        context.config_env.read_file(file)


def get_platform(config_env):
    """
    Retrieves the platform information from the configuration file.

    Args:
        config_env (ConfigParser): The configuration object.

    Returns:
        str: The platform (uppercase).
    """
    try:
        platform = config_env.get("drivers_config", "platform").upper()
        logger.info(f"Platform set to: {platform}")
        return platform
    except Exception as e:
        logger.error(f"Error retrieving platform configuration: {e}")
        raise ValueError("Platform not found in configuration.")


def get_highlight_flag(config_env):
    """
    Retrieves the 'is_highlight' flag from the configuration file and converts it to a boolean.

    Args:
        config_env (ConfigParser): The configuration object.

    Returns:
        bool: True if 'is_highlight' is set to 'true', otherwise False.
    """
    try:
        highlight = convert_string_to_bool(config_env.get("drivers_config", "is_highlight").lower())
        logger.info(f"Highlight flag set to: {highlight}")
        return highlight
    except Exception as e:
        logger.error(f"Error retrieving highlight configuration: {e}")
        raise ValueError("Highlight flag not found in configuration.")


def get_stage_name(config_env):
    """
    Retrieves the stage name from the configuration file.

    Args:
        config_env (ConfigParser): The configuration object.

    Returns:
        str: The stage name (uppercase).
    """
    try:
        stage_name = config_env.get("drivers_config", "stage").upper()
        logger.info(f"Stage name set to: {stage_name}")
        return stage_name
    except Exception as e:
        logger.error(f"Error retrieving stage name: {e}")
        raise ValueError("Stage name not found in configuration.")


def get_browser(config_env):
    """
    Retrieves the browser name from the configuration file, or defaults to 'chrome'.

    Args:
        config_env (ConfigParser): The configuration object.

    Returns:
        str: The browser name.
    """
    try:
        browser = config_env.get("drivers_config", "browser", fallback="chrome")
        logger.info(f"Browser set to: {browser}")
        return browser
    except Exception as e:
        logger.error(f"Error retrieving browser configuration: {e}")
        raise ValueError("Browser not found in configuration.")
def before_scenario(context, scenario):
    """
    This function runs before a scenario is executed.
    It initializes the context based on the specific platform and environment settings.
    """
    try:
        check_tags(scenario)
        if context.platform != 'API':
            device = context.env['devices']
            context.device = list(filter(
                lambda device: device['platformName'] == context.platform, device
            ))
            if len(context.device) == 0:
                logger.error('Framework only is support for chrome, firefox and safari..., trying open with chrome')
            context.device = context.device[0]
            if not context.device['platformName'].upper() in ["WEB", "ANDROID", "IOS"]:
                logger.error(f'Framework only is support for web(firefox, chrome, safari) android and ios..., trying open with chrome')
            context.url = context.env['link']

        context.apiurls = context.env['apifacets']['link']
        context.endpoints = read_configuration().read_api_endpoints()
        logger.info(f'Scenario {scenario.name} started')
        context.dict_yaml = ManagementFile().get_dict_path_yaml()
        context.dict_page_element = {}
    except Exception as e:
        logger.error(str(e) + "with scenario " + scenario.name)

def check_tags(scenario):
    for tag in scenario.tags:
        if tag in ['wip', 'blocked', 'skip', 'manual', 'norun']:
            scenario.mark_skipped()
            logger.warning(f'Scenario {scenario.name} marked as skipped')

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
        logger.error(f"Error occurred in step '{step.name}' of feature '{context.feature.name}'")
        print(f"Error occurred in step '{step.name}' of feature '{context.feature.name}'")
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
        is_remote_saucelabs = convert_string_to_bool(context.config_env.get("drivers_config", "remote-saucelabs").lower())
        if is_remote_saucelabs:
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
                logger.debug(f'can not update status for sauce lab: {str(e)}')
                print('can not update status for sauce lab')
                assert True  # Assert to fail the scenario
        # Quit the driver
        # context.driver.quit()
    # Log the ending of the scenario
    logger.info(f'Scenario {scenario.name} Ended')




def after_all(context):
    # rerun_failed_scenarios(context)
    if context.driver and context.platform == 'WEB':
        logger.info('Closing driver from After_ALL')
        context.driver.close()


def convert_string_to_bool(value):
    """
    Converts a string value to a boolean value.

    Args:
        value (str): The string value to convert.

    Returns:
        bool: The boolean value corresponding to the string value.

    Raises:
        ValueError: If the string value is not 'true' or 'false'.
    """
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")



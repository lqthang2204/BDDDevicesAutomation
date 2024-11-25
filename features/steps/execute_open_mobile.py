import configparser
import os

from selenium.common import SessionNotCreatedException
# from selenium.webdriver.common.devtools.

from project_runner import logger, project_folder
from appium import webdriver as appium_driver
import json
class manage_hook_mobile:
    def open_application(self, context, table):
        """
        Launches the mobile application based on the platform (Android or iOS).

        Args:
            context: The execution context, which contains device and configuration details.
            table: Additional parameters required for driver creation.

        Raises:
            AssertionError: If the platform is unsupported or critical configurations are missing.
        """
        platform_name = context.device.get('platformName', '').strip().upper()
        remote_saucelabs = context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true"

        if not platform_name:
            logger.error("platformName is missing or empty in device configuration.")
            assert False, "platformName is required in device configuration."

        match platform_name:
            case "ANDROID":
                if remote_saucelabs:
                    self.cross_browser_with_mobile(context, context.device, table)
                else:
                    options = self.create_android_driver(context, context.device, table)
                    self.launch_mobile(options, context)

            case "IOS":
                if remote_saucelabs:
                    self.cross_browser_with_mobile(context, context.device, table)
                else:
                    options = self.create_ios_driver(context, context.device, table)
                    self.launch_mobile(options, context)

            case _:
                logger.error(f"Unsupported platformName: {platform_name}. Supported platforms are 'Android' and 'iOS'.")
                assert False, f"Unsupported platformName: {platform_name}. Please use 'Android' or 'iOS'."

        # Common post-launch configuration
        context.wait = context.device.get('wait', 10)  # Default wait to 10 if not specified
        context.highlight = 'false'
        logger.info(f"Application launched successfully on {platform_name}.")

    def cross_browser_with_mobile(self, context, device, table):
        """
        Configures and launches the mobile application in a cross-browser environment using Sauce Labs.

        Args:
            context: The execution context, containing configuration and device details.
            device: Device-specific configurations.
            table: Additional parameters for driver setup.

        Raises:
            ValueError: If required configurations are missing.
        """
        try:
            # Load remote configuration
            config = self.read_config_remote()
            if not config.has_section("remote"):
                raise ValueError("Remote configuration section is missing in the config file.")

            # Retrieve capabilities for the mobile platform
            caps = self.get_data_config_mobile(context, device, table)
            caps['sauce:options'] = {}

            # Load Sauce Labs options
            required_keys = ["username", "accessKey", "build", "name", "url"]
            for key in required_keys:
                if not config.get("remote", key, fallback=None):
                    raise ValueError(f"Missing required Sauce Labs config key: '{key}'.")

            caps['sauce:options'].update({
                'appiumVersion': '2.0.0',
                'username': config.get("remote", "username"),
                'accessKey': config.get("remote", "accessKey"),
                'build': config.get("remote", "build"),
                'name': config.get("remote", "name"),
                'deviceOrientation': 'PORTRAIT'
            })

            # Set context attributes
            context.wait = device.get('wait', 0)  # Default to 0 if not specified
            context.device = device

            # Initialize driver options and load capabilities
            from appium.options.android import UiAutomator2Options
            from appium.options.ios import XCUITestOptions

            if device['platformName'].strip().upper() == "ANDROID":
                options = UiAutomator2Options()
            elif device['platformName'].strip().upper() == "IOS":
                options = XCUITestOptions()
            else:
                raise ValueError(f"Unsupported platform: {device['platformName']}")

            options.load_capabilities(caps)

            # Establish the remote Appium driver
            remote_url = config.get("remote", "url")
            context.driver = appium_driver.Remote(remote_url, options=options)

            logger.info(f"Cross-browser mobile session started successfully on {device['platformName']}.")
        except Exception as e:
            logger.error(f"Failed to start cross-browser mobile session: {str(e)}")
            raise

    import os
    import json
    import logging

    logger = logging.getLogger(__name__)

    def get_data_config_mobile(self, context, device, table):
        """
        Retrieves mobile-specific configuration data from a JSON file.

        Args:
            context: The execution context, containing paths and configuration details.
            device: Device-specific information (not directly used but kept for potential extensions).
            table: A list containing the configuration file name as the first element.

        Returns:
            dict: Parsed configuration data from the specified JSON file.
                  Returns an empty dictionary or raises an exception if the file cannot be processed.

        Raises:
            ValueError: If the JSON file contains invalid data or is missing critical keys.
        """
        if not table or not table[0]:
            logger.error("Table is missing or does not contain a valid configuration file name.")
            raise ValueError("Configuration file name is required in the table parameter.")

        config_file_path = os.path.join(context.root_path, "configuration_env", f"{table[0][0]}.json")

        try:
            # Attempt to load the configuration file
            with open(config_file_path, 'r') as file:
                config_data = json.load(file)
                logger.info(f"Successfully loaded configuration from {config_file_path}.")
                return config_data

        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_file_path}.")
            # Return a default configuration or raise an exception
            return {}

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON file: {config_file_path}. Error: {str(e)}")
            # Return a default configuration or raise an exception
            return {}

        except Exception as e:
            logger.error(f"Unexpected error while loading configuration: {str(e)}")
            raise

    import os
    import configparser
    import logging

    logger = logging.getLogger(__name__)

    def read_config_remote(self):
        """
        Reads and parses the remote configuration file.

        Returns:
            configparser.RawConfigParser: The parsed configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            configparser.Error: If there is an error in parsing the configuration file.
        """
        config_file_path = os.path.join(project_folder, 'config_env.ini')

        # Create a RawConfigParser object
        config = configparser.RawConfigParser(allow_no_value=True)

        try:
            # Attempt to open and read the configuration file
            with open(config_file_path, 'r') as file:
                config.read_file(file)
                logger.debug(f"Configuration file loaded successfully: {config_file_path}")
                return config

        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_file_path}")
            raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

        except configparser.MissingSectionHeaderError:
            logger.error(f"Configuration file missing section headers: {config_file_path}")
            raise configparser.MissingSectionHeaderError(
                f"Missing section headers in configuration file: {config_file_path}"
            )

        except configparser.ParsingError as e:
            logger.error(f"Error parsing configuration file: {config_file_path}. Error: {e}")
            raise configparser.ParsingError(f"Error parsing configuration file: {config_file_path}")

        except Exception as e:
            logger.error(f"Unexpected error reading configuration file: {config_file_path}. Error: {e}")
            raise

    def launch_mobile(self, options, context):
        try:
            appium_url = self.check_att_exist(options, "appium_url")
            context.driver = appium_driver.Remote(appium_url, options = options)
        except SessionNotCreatedException as ex:
            logger.error('Config file updated based on user provided command line arguments')
            assert False, f'{ex.msg}'
    def check_att_exist(self, obj, key):
        if obj.get_capability(key) is None or obj.get_capability('appium:'+key) is None:
            return "127.0.0.1:4723"
        else:
            try:
                return obj.get_capability(key)
            except Exception as e:
                logger.error(f"please check file input json: {str(e)}")
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
            logger.error(f"An error occurred while navigating to URL: {str(e)} on device {context.device['platformName'].upper()}")



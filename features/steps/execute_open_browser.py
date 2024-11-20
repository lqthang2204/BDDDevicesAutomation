import os
from selenium import webdriver
from selenium.common import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as chrome_option
from selenium.webdriver.chrome.service import Service as chrome_service
from selenium.webdriver.firefox.options import Options as firefox_option
from selenium.webdriver.firefox.service import Service as firefox_service
from selenium.webdriver.safari.options import Options as safari_option
from selenium.webdriver.safari.service import Service as safari_service
from project_runner import logger, project_folder
from execute_open_mobile import manage_hook_mobile as manage_remote


class manage_hook_browser:
    def open_browser(self, context, table, name):
        """
        Opens a browser based on the context provided.

        Args:
        - self: the class instance
        - context: the context containing device and configuration information
        - table: the table to interact with
        - name: the name of the browser to open
        """

        # Check if the device is set to run in headless mode
        if context.device['is_headless']:
            context.highlight = 'false'

        # Check if running on remote Saucelabs for cross-browser testing
        if context.config_env.get("drivers_config", "remote-saucelabs").lower() == "true":
            self.cross_browser_with_web(context, context.device, table, name)
        else:
            # Launch the browser based on the provided context
            self.launch_browser(context, context.device, context.browser, table, name)

    def launch_browser(self, context, device, browser, table, name):
        """
        Launches a browser based on the provided context and configuration.

        Args:
            - self: the class instance
            - context: the context containing device and configuration information
            - device: the device information
            - browser: the browser type
            - table: the table to interact with
            - name: the name of the browser to open
        """

        # Step 1: Get browser-specific options
        option = self.get_option_from_browser(context, browser, device, table)

        # Step 2: Initialize the WebDriver if not already initialized
        if context.driver is None:
            try:
                self._initialize_driver(context, browser, device, option)

                # Step 3: Set page load and wait time based on the device configuration
                context.wait = self.check_attr_exist(device, 'wait')
                context.time_page_load = self.check_attr_exist(device, 'time_page_load')

                # Step 4: Maximize window if not explicitly specified
                if not any("--window-size" in argument for argument in option.__getattribute__("arguments")):
                    context.driver.maximize_window()

            except SessionNotCreatedException as e:
                logger.error(f"Failed to initialize the browser driver: {e}")
                assert False, f"Failed to initialize the browser driver: {e}"
            except Exception as e:
                logger.error(f"Unexpected error occurred during driver initialization: {e}")
                assert False, f"Unexpected error occurred: {e}"

        # Step 5: Open the correct URL in the browser
        self._open_url_in_browser(context, name)

    def _initialize_driver(self, context, browser, device, option):
        """
        Initializes the WebDriver based on the provided browser and device configuration.
        """
        # Check if the device requires auto-download of the driver
        if 'auto_download_driver' in device and not device.get('auto_download_driver', True):
            self.get_driver_from_path(context, browser, device, option)
        else:
            # Initialize the driver based on the browser type
            match browser.upper():
                case 'CHROME':
                    context.driver = webdriver.Chrome(options=option)
                case 'FIREFOX':
                    context.driver = webdriver.Firefox(options=option)
                case 'SAFARI':
                    context.driver = webdriver.Safari()
                case _:
                    logger.warning(f"Unsupported browser '{browser}', defaulting to Chrome.")
                    context.driver = webdriver.Chrome(options=option)

    def _open_url_in_browser(self, context, name):
        """
        Opens the URL corresponding to the given name in the browser.
        """
        try:
            # Handle special cases like KEY.* URLs
            if 'KEY.' in name:
                temp_url = context.dict_save_value.get(name)
                if temp_url:
                    context.driver.get(temp_url)
                else:
                    logger.error(f"URL for '{name}' not found in saved values.")
                    assert False, f"URL for '{name}' not found in saved values."
            else:
                url_to_open = context.url.get(name)
                if url_to_open:
                    context.driver.get(url_to_open)
                else:
                    logger.error(f"URL '{name}' not found in environment settings.")
                    assert False, f"URL '{name}' not found in environment settings."

        except Exception as e:
            logger.error(f"Failed to open browser with URL '{name}': {e}")
            assert False, f"Failed to open browser with URL '{name}': {e}"

    def get_driver_from_path(self, context, browser, device, option):
        """
        This function gets the driver from the path based on the browser type and device.

        Args:
        - context: the context containing device and configuration information
        - browser: the browser type
        - device: the device information
        - option: the options to set for the driver
        """

        # Update the service based on the browser type and device driver path
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
            # Log a message and try to open with chrome
            logger.info('Framework only is support for chrome, firefox and safari..., trying open with chrome')
            service = chrome_service(
                executable_path=project_folder + '\\' + device['driver_version'])
            context.driver = webdriver.Chrome(service=service, options=option)

    import os

    def get_option_from_browser(self, context, browser, device, table):
        """
        Get browser options based on the browser type and additional parameters provided in the table.

        Args:
            context (object): The context object.
            browser (str): The browser type.
            device (dict): The device information.
            table (list): The list of additional parameters.

        Returns:
            option: The browser options object.
        """
        # Define supported browsers and their corresponding option methods
        supported_browsers = {
            'chrome': chrome_option,
            'firefox': firefox_option,
            'safari': safari_option,
        }

        # Get the option based on the browser type, default to chrome_option if not found
        option_func = supported_browsers.get(browser.lower())
        if option_func:
            option = option_func()
            if browser.lower() == 'safari':
                option.SAFARI_TECH_PREVIEW = True
        else:
            logger.error(f'Unsupported browser: {browser}')
            assert False, f'Unsupported browser: {browser}'

        # Process additional parameters from the table
        if table:
            for rows in table:
                if rows[0] == 'argument' and hasattr(option, 'add_argument'):
                    option.add_argument(rows[1])
                elif rows[0] == 'extension' and hasattr(option, 'add_extension'):
                    folder_path = os.path.join(context.root_path, 'extensions/')
                    option.add_extension(folder_path + rows[1])
                else:
                    logger.error(
                        f'feature use extension and argument only support for chrome not support for {browser.lower()} browser')
                    assert False, f'Framework only is support for argument, extension parameter not support for {rows[0]}'

        # Add headless mode if specified for Chrome or Firefox
        if device['is_headless'] and browser.lower() in ['chrome', 'firefox']:
            option.add_argument('--headless')
        if device['is_headless'] and browser.lower() == 'safari':
            logger.info(f'Safari does not support headless mode, please use chrome or firefox instead')
            print(f'Safari does not support headless mode, please use chrome or firefox instead')
        return option



    def cross_browser_with_web(self, context, device, table, name):
        """
        This function sets up a remote web driver for cross-browser testing.

        Args:
        - context: the context object containing driver and URL information
        - device: the device configuration for the test
        - table: table information for the test
        - name: the name of the URL to navigate to

        Returns:
        - None
        """

        if context.driver is None:
            # Read remote configuration
            config = manage_remote().read_config_remote()

            # Get browser options based on remote config
            options = self.get_option_from_browser(context, config.get("remote", "browser"), device, table)

            # Set browser version and platform name
            options.browser_version = 'latest'
            options.platform_name = config.get("remote", "platform_name")

            # Set Sauce Labs options
            sauce_options = {
                'username': config.get("remote", "username"),
                'accessKey': config.get("remote", "accessKey"),
                'build': config.get("remote", "build"),
                'name': config.get("remote", "name")
            }
            options.set_capability('sauce:options', sauce_options)

            # Get remote URL and initialize driver
            url = config.get("remote", "url")
            context.driver = webdriver.Remote(command_executor=url, options=options)

            # Set up context variables
            context.wait = device['wait']
            context.device = device
            context.time_page_load = device['time_page_load']

            # Maximize window
            context.driver.maximize_window()

        # Navigate to the specified URL

            context.driver.get(context.url[name])
        elif 'KEY.' in name and context.driver is not None:
            temp_url = context.dict_save_value[name]
            context.driver.get(temp_url)

        else:
            context.driver.get(context.url[name])

    def check_attr_exist(self, device, label):
        """
        Checks if the specified attribute exists in the device configuration.

        Args:
            device (dict): The device configuration dictionary.
            label (str): The attribute to check in the device configuration.

        Returns:
            int: The value of the attribute if it exists, otherwise returns 30.

        Raises:
            AssertionError: If the attribute is not supported in the framework.
        """
        # Check for specific attributes in the device configuration
        if label == "wait":
            if label in device:
                return device[label]
            else:
                return 30
        elif label == "time_page_load":
            if hasattr(device, label):
                return device[label]
            else:
                return 30
        else:
            logger.error(f'attribute {label} not supported in the framework')
            assert False, f'attribute {label} not supported in the framework'


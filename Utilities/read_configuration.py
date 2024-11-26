import json
import os

import yaml
from yaml import SafeLoader

from project_runner import project_folder, logger


class read_configuration:
    def read(self, stage_name):
        """
           Reads the configuration file and returns the environment settings for the given stage.
           Args:
               stage_name (str): The name of the stage to retrieve settings for.
           Returns:
               dict: The environment settings for the given stage.
           """
        # Construct the path to the configuration file
        try:
            config_file_path = os.path.join(project_folder, "environments.yml")
            with open(config_file_path) as configs_env:
                config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
                if not config_file:
                    return {}
                    # Convert the configuration file to JSON and extract the 'env' list
                json_result = json.dumps(config_file)
                arr_stage = json.loads(json_result)['env']
                # Find the environment settings for the given stage
                for stage_env in arr_stage:
                    if stage_env['stage'] == stage_name:
                        return stage_env
            # Return an empty dictionary if the stage is not found
            return {}
        except FileNotFoundError:
            # If the YAML file is not found, raise an error
            raise FileNotFoundError(f"API endpoints file not found at {stage_name}")
        except yaml.YAMLError as e:
            # If there is an error parsing the YAML file, raise an error
            raise yaml.YAMLError(f"Error parsing API endpoints file at {stage_name}: {str(e)}")

    def read_api_endpoints(self):
        """
    This method reads the API endpoints from the YAML file and returns them.

    Returns:
        dict: The API endpoints.

    Raises:
        FileNotFoundError: If the API endpoints YAML file is not found.
        yaml.YAMLError: If there is an error parsing the YAML file.
    """
        # Define the path to the API endpoints YAML file
        api_endpoint_path = os.path.join(project_folder, "resources", "api", "endpoints", 'api-endpoints.yml')
        try:
            with open(api_endpoint_path) as api_endpoints_file:
                api_endpoint = yaml.safe_load(api_endpoints_file.read())
        except FileNotFoundError:
            # If the YAML file is not found, raise an error
            raise FileNotFoundError(f"API endpoints file not found at {api_endpoint_path}")
        except yaml.YAMLError as e:
            # If there is an error parsing the YAML file, raise an error
            raise yaml.YAMLError(f"Error parsing API endpoints file at {api_endpoint_path}: {str(e)}")
        return api_endpoint

    def get_content_javascript(self, root_path, javascript):
        """
        Reads the content of a JavaScript file.

        Args:
            root_path (str): The root path where the JavaScript file is located.
            javascript (str): The name of the JavaScript file (without the extension).

        Returns:
            str: The content of the JavaScript file.

        Raises:
            FileNotFoundError: If the JavaScript file does not exist.
            IOError: If there is an issue reading the file.
        """
        try:
            # Construct the full path to the JavaScript file
            config_file_path = os.path.join(root_path, "javascripts", f"{javascript}.js")
            logger.info(f"Attempting to read JavaScript file: {config_file_path}")

            # Check if the file exists
            if not os.path.exists(config_file_path):
                logger.error(f"JavaScript file not found: {config_file_path}")
                raise FileNotFoundError(f"JavaScript file not found: {config_file_path}")

            # Read and return the file content
            with open(config_file_path, "r", encoding="utf-8") as dataFile:
                data = dataFile.read()
                logger.info(f"Successfully read JavaScript file: {config_file_path}")
                return data

        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError: {str(e)}")
            raise
        except IOError as e:
            logger.error(f"IOError while reading the file: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            raise

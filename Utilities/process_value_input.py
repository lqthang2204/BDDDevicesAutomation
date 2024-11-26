import re
from libraries.data_generators import check_match_pattern, get_test_data_for
from libraries.faker import management_user
from project_runner import logger
class procees_value:
    import re


    def get_value(self, value_input: str, dict_save_value: dict) -> str:
        """
        Process a value string to substitute placeholders with corresponding values.

        Args:
            value_input (str): The input string containing placeholders to be replaced.
            dict_save_value (dict): A dictionary containing saved values for substitution.

        Returns:
            str: The processed string with placeholders replaced by actual values.

        Raises:
            RuntimeError: If an error occurs during value processing.
        """
        try:
            if not value_input:
                logger.warning("Received an empty or None value_input.")
                return ""

            # Handle placeholder patterns like {PLACEHOLDER}
            if re.search(r"\{.*?\}", value_input):
                logger.debug(f"Processing placeholders in value_input: {value_input}")
                value_input = re.sub(r"[{}]", "$", value_input)  # Replace curly braces with '$'
                parts = value_input.split('$')
                value_input = "".join([get_test_data_for(item, dict_save_value) for item in parts])

            # Handle USER. prefix logic
            if "USER." in value_input:
                logger.debug(f"Processing USER. placeholder in value_input: {value_input}")
                value_input = self.get_value_from_user_random(value_input, dict_save_value)

            # Retrieve value from dictionary if available
            if dict_save_value and value_input in dict_save_value:
                logger.debug(f"Fetching value from dict_save_value for key: {value_input}")
                value_input = dict_save_value.get(value_input, value_input)

            return value_input

        except Exception as e:
            logger.error(f"An error occurred while processing value_input '{value_input}': {e}", exc_info=True)
            raise RuntimeError(f"Error processing value_input '{value_input}'.") from e

    def get_value_from_user_random(self, value: str, dict_save_value: dict) -> str:
        """
        Retrieve a value associated with a user key from a saved dictionary.

        Args:
            value (str): The input string containing 'USER.' followed by a key.
            dict_save_value (dict): A dictionary containing user-related data.

        Returns:
            str: The value associated with the specified user key.

        Raises:
            KeyError: If the 'USER.' key is not found in `dict_save_value`.
            ValueError: If the input format is invalid or the key is missing.
            RuntimeError: For any other unexpected errors.
        """
        try:
            # Validate the presence of 'USER.' in the saved dictionary
            if 'USER.' not in dict_save_value:
                raise KeyError("The key 'USER.' is not present in the provided dictionary.")

            # Split the input string on 'USER.' and validate its structure
            arr_user = value.split('USER.')
            if len(arr_user) < 2 or not arr_user[1].strip():
                raise ValueError(
                    f"Invalid format for value '{value}'. Expected format: 'USER.<key>'."
                )

            user_key = arr_user[1].strip()
            list_user = dict_save_value['USER.']

            # Retrieve the user value
            user_value = management_user.get_user(list_user, user_key)
            logger.info(f"Retrieved value '{user_value}' for user key '{user_key}' successfully.")
            return user_value

        except KeyError as ke:
            logger.error(f"KeyError: {ke}")
            raise

        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            raise RuntimeError(f"Error retrieving user value for '{value}': {e}") from e

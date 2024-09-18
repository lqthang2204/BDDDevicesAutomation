import re
from libraries.data_generators import check_match_pattern, get_test_data_for
from libraries.faker import management_user
import logging
class procees_value:
    def get_value(self, value_input, dict_save_value):
        result = re.search(r"\{.*?\}", value_input)
        if result:
            value_input = re.sub("[{}]", "$", value_input)
            value_input = value_input.split('$')
            value_input = "".join([get_test_data_for(item, dict_save_value) for item in value_input])
        if 'USER.' in value_input:
            value_input = self.get_value_from_user_random(value_input, dict_save_value)
        if dict_save_value:
            value_input = dict_save_value.get(value_input, value_input)
        return value_input

    def get_value_from_user_random(self, value, dict_save_value):
        try:
            if 'USER.' not in dict_save_value:
                raise KeyError("'USER.' key not found in dict_save_value")

            arr_user = value.split('USER.')
            list_user = dict_save_value['USER.']
            if len(arr_user) < 2:
                raise ValueError("Invalid format for value. Expected 'USER.' followed by a key.")
            value = management_user.get_user(list_user, arr_user[1])
            logging.info(f"Value '{value}' retrieved successfully for key '{arr_user[1]}'")
            return value
        except KeyError as ke:
            logging.error(f"KeyError: {ke}")
            raise
        except ValueError as ve:
            logging.error(f"ValueError: {ve}")
            raise
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise
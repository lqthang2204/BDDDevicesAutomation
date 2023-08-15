import json
import re

from jsonpath_ng import parse
from requests import Response

from libraries.data_generators import get_test_data_for


class APIAsserts:

    def status_code(response: Response, expected_code: int, message: str = None):
        assert response.status_code == expected_code, \
            f'Expected status code {expected_code}, but got {response.status_code}. {message}'

    def response_has_key(response_dict, context, table, status_code, title):
        try:
            if title == "response_code":
                assert response_dict['code'] == int(
                    status_code), f'response status code failed when return {response_dict["code"]}'
            else:
                if table:
                    if title == "header":
                        for row in table:
                            print("verifying header api")
                            field_name = row[0]
                            field_value = get_test_data_for(row[1], context.dict_save_value)
                            helpers = row[2]
                            value_header = response_dict['headers'][field_name]
                            if helpers.startswith('KEY'):
                                context.dict_save_value[helpers] = value_header
                            elif len(field_value) == 0 and field_name:
                                if helpers != "":
                                    value = APIAsserts.check_condition_have_result_body("", helpers, value_header)
                                # if helper = '', default key always have value !=""
                                else:
                                    assert value != "", f'Response json does not contain field name {value_header}'
                            elif field_value != "" and field_name:
                                if helpers == "REGEX":
                                    assert re.search(field_value,
                                                     value_header), f'Response json does not match with pattern at {value_header}'
                                else:
                                    # assert field_value == value, f'Response json does not have a value {field_value}'
                                    APIAsserts.check_condition_have_result_body(field_value, helpers, value_header)
                    elif title == "body":
                        for row in table:
                            print("verifying body api")
                            field_name = row[0]
                            field_value = get_test_data_for(row[1], context.dict_save_value)
                            helpers = row[2]
                            data = response_dict['json']
                            # get data from key
                            value_body = APIAsserts.find_value_from_key(data, field_name)
                            if helpers.startswith('KEY'):
                                context.dict_save_value[helpers] = value_body
                            elif len(field_value) == 0 and field_name:
                                # check data , if helper !=", check data based to helper
                                if helpers != "":
                                    APIAsserts.check_condition_have_result_body("", helpers, value_body)
                                # if helper = '', default key always have value !=""
                                else:
                                    assert value_body != "", f'Response json does not contain field name {data}'
                            elif len(field_value) != 0 and field_name or helpers:
                                if context.dict_save_value:
                                    field_value = context.dict_save_value.get(field_value, field_value)
                                if helpers == "REGEX":
                                    if isinstance(value_body, list):
                                        for val in value_body:
                                            assert re.search(field_value,
                                                             val), f'Response json does not match with pattern at {val}'
                                    else:
                                        assert re.search(field_value,
                                                         value_body), f'Response json does not match with pattern at {value_body}'
                                else:
                                    # assert field_value == value, f'Response json does not have a value {field_value}'
                                    APIAsserts.check_condition_have_result_body(field_value, helpers, value_body)

        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format'

    def find_value_from_key(json_object, target_key):
        try:
            if re.search('[*]', target_key):
                jsonpath_expression = parse(target_key)
                match_value_list = [match.value for match in jsonpath_expression.find(json_object)]
                return match_value_list
            else:
                jsonpath_expression = parse(target_key)
                match = jsonpath_expression.find(json_object)
                return match[0].value
        except Exception as e:
            print("not found value from key")
            return ""

    def check_condition_have_result_body(field_value, helpers, value):
        if helpers == "NUMERIC":
            assert str(value).isnumeric(), f'Response json does not contain number have value {value}'
        elif helpers == "ALPHABET":
            assert str(value).isalpha(), f'Response json does not contain alphabet {value}'
        elif helpers == "NOT_NULL":
            assert value is not None, f'Response json does not contain a field name {value}'
        elif helpers == "CONTAIN" and field_value != "":
            assert field_value in value, f'Response json does not contain a field name {value}'
        elif helpers == "EQUAL" and field_value != "":
            assert field_value == value, f'Response json does not equal a field name {value}'
        elif helpers == "":
            # when helper = "" => default is check value same with value of key
            assert field_value == value, f'Response json does not equal a field name {value}'
        else:
            assert False, f'not contain helper in data table do not check'

    # def get_json_file(self, data_payload, target_key, value, dict_save_value):
    #     if dict_save_value:
    #         value = dict_save_value.get(value, value)
    #     jsonpath_expression = parse(target_key)
    #     jsonpath_expression.find(data_payload)
    #     data_payload = jsonpath_expression.update(data_payload, value)
    #     return data_payload

import json
import re

from jsonpath_ng import parse
from requests import Response
from libraries.data_generators import get_test_data_for
from project_runner import logger
from libraries.data_generators import check_match_pattern

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
                            logger.info("verifying header api")
                            field_name = row[0]
                            field_value = get_test_data_for(row[1], context.dict_save_value)
                            helpers = row[2]
                            value_header = response_dict['headers'][field_name]
                            logger.info(f'header value : {value_header}')
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
                                    check_match_pattern(field_value, value_header, 'Response json does not match with pattern at')
                                else:
                                    # assert field_value == value, f'Response json does not have a value {field_value}'
                                    APIAsserts.check_condition_have_result_body(field_value, helpers, value_header)
                    elif title == "body":
                        logger.info("verifying body api")
                        for row in table:
                            if row[0] == 'response_code':
                                continue
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
                                            check_match_pattern(field_value, val, 'Response json does not match with pattern at')
                                    else:
                                        check_match_pattern(field_value, value_body, 'Response json does not match with pattern at')
                                else:
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
            logger.error("not found value from key")
            return ""

    def check_condition_have_result_body(field_value, helpers, value):
        if helpers == "NUMERIC":
            if field_value != "" and isinstance(value, list):
                for val in value:
                    assert str(val).isnumeric(), f'Response json does not number have value {value}'
                assert int(field_value) in value, f'Response json does not contain number have value {value}'
            elif field_value != "":
                assert int(field_value) == value, f'Response json does not equal number have value {value}'
            elif field_value == "" and isinstance(value, list):
                for val in value:
                    assert str(val).isnumeric(), f'Response json does not number have value {value}'
            else:
                assert str(value).isnumeric(), f'Response json does not number have value {value}'
        elif helpers == "ALPHABET":
            if field_value != "" and isinstance(value, list):
                for val in value:
                    assert str(val).isalpha(), f'Response json does not alpha have value {value}'
                assert field_value in value, f'Response json does not contain alpha have value {value}'
            elif field_value != "":
                assert field_value == value, f'Response json does not equal alpha have value {value}'
            elif field_value == "" and isinstance(value, list):
                for val in value:
                    assert str(val).isalpha(), f'Response json does not alpha have value {value}'
            else:
                assert str(value).isalpha(), f'Response json does not alpha have value {value}'
        elif helpers == "NOT_NULL":
            assert value is not None, f'Response json does not contain a field name {value}'
        elif helpers == "CONTAIN":
            if field_value != "" and isinstance(value, list):
                for val in value:
                    assert field_value in val, f'Response json does not contain have value {value}'
            elif field_value != "":
                assert field_value in value, f'Response json does not equal alpha have value {value}'
            else:
                assert False, f'Not found expected value in datatable {field_value}'
        elif helpers == "BOOL" and field_value != "":
            if field_value != "" and isinstance(value, list):
                for val in value:
                    assert type(val) == bool, f'Response json does not contain boolean {value}'
                assert APIAsserts.convert_string_to_bool(
                    field_value) in value, f'Response json does not contain a field name {value}'
            elif field_value != "":
                assert APIAsserts.convert_string_to_bool(
                    field_value) == value, f'Response json does not contain a field name {value}'
            elif field_value == "" and isinstance(value, list):
                for val in value:
                    assert type(val) == bool, f'Response json does not contain boolean {value}'
            else:
                assert type(value) == bool, f'Response json does not boolean {value}'
        elif helpers == "EQUAL" and field_value != "":
            if field_value != "" and isinstance(value, list):
                for val in value:
                    assert field_value == val, f'Response json does not equal a field name {value}'
            elif field_value != "":
                assert field_value == value, f'Response json does not equal a field name {value}'
            else:
                assert False, f'Not found expected value in datatable {field_value}'
        elif helpers == "":
            if field_value != "":
                # when helper = "" => default is check value same with value of key
                assert field_value == value, f'Response json does not equal a field name {value}'
            else:
                assert False, f'Not found expected value in datatable {field_value}'
        else:
            assert False, f'not contain helper in data table do not check'

    def convert_string_to_bool(expect):
        if expect in ['true', 'True', 'TRUE']:
            return True
        elif expect in ['false', 'False', 'FALSE']:
            return False
        else:
            assert False, f'framework does not support convert type bool as {expect}'


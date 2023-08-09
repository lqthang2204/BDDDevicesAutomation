import json

from requests import Response
import os


class APIAsserts:


    def status_code(response: Response, expected_code: int, message: str = None):
        assert response.status_code == expected_code, \
            f'Expected status code {expected_code}, but got {response.status_code}. {message}'


    def response_has_key(response: Response, table, status_code, title):
        try:
            if title == "response_code":
                assert response.status_code == int(status_code), f'response status code failed when return {response.status_code}'
            else:
                if table:
                    if title == "header":
                        for row in table:
                            print("verifying header api")
                            field_name = row[0]
                            field_value = row[1]
                            helpers = row[2]
                            if len(field_value) == 0 and field_name:
                                APIAsserts.check_condition_not_result(field_name, helpers, dict(response.headers))
                            elif len(field_value) != 0 and field_name or helpers:
                                assert field_value in dict(response.headers)[field_name], f'Response json does not have value {field_value}'
                                APIAsserts.check_condition_have_result(dict(response.headers)[field_name], helpers)
                    elif title == "body":
                        for row in table:
                            print("verifying body api")
                            field_name = row[0]
                            field_value = row[1]
                            helpers = row[2]
                            data = response.json()
                            list_value = []
                            if len(field_value) == 0 and field_name:
                                list_value = APIAsserts.find_value_from_key(data, field_name, list_value)
                                APIAsserts.check_condition_not_result_body(field_name, helpers, list_value)
                            elif len(field_value) != 0 and field_name or helpers:
                                list_value = APIAsserts.find_value_from_key(data, field_name, list_value)
                                assert field_value in list_value,  f'Response json does not have a value {field_value}'
                                APIAsserts.check_condition_have_result_body(field_value, helpers, list_value)

                                # value = dict(response.headers)]
                                # assert value in data_header[1].strip(), f'Response json does not have a value {value}'

        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format'

    def find_value_from_key(json_object, target_key, list_test):
        if type(json_object) is dict and json_object:
            for key in json_object:
                if key == target_key:
                    print("{}: {}".format(target_key, json_object[key]))
                    list_test.append(str(json_object[key]))
                APIAsserts.find_value_from_key(json_object[key], target_key, list_test)

        elif type(json_object) is list and json_object:
            for item in json_object:
                APIAsserts.find_value_from_key(item, target_key, list_test)
        return list_test
    def check_condition_have_result(result, helpers):
        if helpers == "NUMERIC":
            return result.isnumeric()
        elif helpers == "ALPHABET":
            return result.isalpha()
        elif helpers == "NOT_NULL":
            return result is not None
        elif helpers == "NULL":
            return result is None
        else:
            print("not contain helper in data table do not check")
    def check_condition_not_result(field_name, helpers, response_header):
        if helpers == "NOT_NULL":
            assert field_name in response_header, f'Response json does not contain a field name {field_name}'
        elif helpers == "NULL":
            assert response_header.get(field_name) is None , f'Response json contain a field name {field_name}'
        elif helpers == "NUMERIC":
            return response_header.get(field_name).isnumeric() , f'Response json does not contain number {response_header.get(field_name).isnumeric()}'
        elif helpers == "ALPHABET":
            return response_header.get(field_name).isalpha(), f'Response json does not contain alphabet {response_header.get(field_name).isnumeric()}'

    def check_condition_have_result_body(result, helpers, list_value):
        if helpers == "NUMERIC":
            assert result.isnumeric(), f'Response json does not contain number have value {result}'
        elif helpers == "ALPHABET":
            assert result.isalpha(), f'Response json does not contain alphabet {result}'
        elif helpers == "NOT_NULL":
            assert list_value is not None, f'Response json does not contain a field name {result}'
        elif helpers == "NULL":
            assert result is None, f'Response json contain a field name {result}'

    def check_condition_not_result_body(field_name, helpers, list_value):
        if helpers == "NOT_NULL":
            assert len(list_value) > 0, f'Response json does not contain a field name {field_name}'
        elif helpers == "NULL":
            assert len(list_value) == 0, f'Response json contain a field name {field_name}'
        elif helpers == "NUMERIC":
            if list_value:
                for key in list_value:
                    assert key.isnumeric(), f'Response json does not contain number have value {key}'
        elif helpers == "ALPHABET":
            if list_value:
                for key in list_value:
                    assert key.isalpha(), f'Response json does not contain alphabet {key}'

import json

from requests import Response
import os


class APIAsserts:


    def status_code(response: Response, expected_code: int, message: str = None):
        assert response.status_code == expected_code, \
            f'Expected status code {expected_code}, but got {response.status_code}. {message}'


    def response_has_key(response: Response, table):
        try:
            if table:
                for row in table:
                    if row['FieldName'] == 'Response Code':
                        print("verifying response code api")
                        assert response.status_code == int(row["FieldValue"]), f'response status code failed when return {response.status_code}'
                    if row['FieldName'] == 'Response Header':
                        print("verifying header api")
                        data_header = row["FieldValue"].split("Equal")
                        value = dict(response.headers)[data_header[0].strip()]
                        assert value in data_header[1].strip(), f'Response json does not have a value {value}'
                    if row['FieldName'] == 'Response Body':
                        print("verifying body api")
                        data = response.json()
                        data_header = row["FieldValue"].split("Equal")
                        list_value = []
                        list_value = APIAsserts.find_value_from_key(data,data_header[0].strip(), list_value)
                        print("list value ", list_value)
                        assert data_header[1].strip() in list_value, f'Response json does not have a value {value}'
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

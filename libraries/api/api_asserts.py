import json

from requests import Response


class APIAsserts:

    @staticmethod
    def status_code(response: Response, expected_code: int, message: str = None):
        assert response.status_code == expected_code, \
            f'Expected status code {expected_code}, but got {response.status_code}. {message}'

    @staticmethod
    def response_has_key(response: Response, key: str):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format'
        assert key in response_as_dict, f'Response json does not have a key {key}'

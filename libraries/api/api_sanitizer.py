import re


class RequestProps:

    def __init__(self):
        self.headers = None
        self.payload = None
        self.cookies = None
        self.params = None

    @classmethod
    def _sanitize_headers(cls):
        if cls._headers:
            cls._headers = {key.strip(): value.strip() for key, value in cls._headers.items()}

    @classmethod
    def _get_headers(cls):
        return cls._headers

    @classmethod
    def _set_headers(cls, headers):
        cls._headers = headers
        cls._sanitize_headers()  # Call the sanitize method whenever headers are set

    @property
    def headers(self):
        return self._get_headers()

    @headers.setter
    def headers(self, headers):
        self._set_headers(headers)

    @classmethod
    def _sanitize_payload(cls):
        if cls._payload:
            cls._payload = re.sub(r'\s*"\s*(.*?[^\\])\s*"\s*', r'"\1"', cls._payload, flags=re.DOTALL)
            cls._payload = re.sub(r'\s*([{}:\[\]])\s*', r'\1', cls._payload, flags=re.DOTALL)

    @classmethod
    def _get_payload(cls):
        return cls._payload

    @classmethod
    def _set_payload(cls, payload):
        cls._payload = payload
        cls._sanitize_payload()  # Call the sanitize method whenever payload are set

    @property
    def payload(self):
        return self._get_payload()

    @payload.setter
    def payload(self, payload):
        self._set_payload(payload)

    @property
    def params(self):
        return self._get_params()

    @params.setter
    def params(self, params):
        self._set_params(params)

    @classmethod
    def _get_params(cls):
        return cls._params

    @classmethod
    def _set_params(cls, params):
        cls._params = params
        cls._sanitize_params()  # Call the sanitize method whenever params are set

    @classmethod
    def _sanitize_params(cls):
        if cls._params:
            cls._params = [item.strip() for item in cls._params]


if __name__ == '__main__':
    # Usage:
    just_collected_headers = {
        "       Content-Type       ": "     application/json       ",
        "       Authorization         ": "      Bearer my_token      ",
    }

    # Create an instance of the Requestz class
    request_instance = RequestProps()

    # Assign headers and the sanitize function will be triggered automatically
    request_instance.headers = just_collected_headers

    print(request_instance.headers)

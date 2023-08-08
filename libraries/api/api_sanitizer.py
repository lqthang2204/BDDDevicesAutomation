import re
class RequestProps:
    _headers = {}
    _payload = {}

    @classmethod
    def _sanitize_headers(cls):
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
        cls._payload = cls._payload.replace('\n', '')

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

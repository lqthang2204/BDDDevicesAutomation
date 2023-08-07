class RequestProps:
    _headers = {}

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

#
# class CheckRequest(RequestProps):
#
#     @staticmethod
#     def __init__():
#         super().headers = {
#         "       Content-Type       ": "     application/json       ",
#         "       Authorization         ": "      Bearer my_token      ",
#     }
#
#     @staticmethod
#     def _sendthis():
#         print(CheckRequest.headers)

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

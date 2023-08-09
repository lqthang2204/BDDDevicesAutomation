import requests

from libraries.api.api_sanitizer import RequestProps


class Requests(RequestProps):
    def __init__(self, context=None, apifacet_name=None, endpoint_name=None):
        super().__init__()
        if apifacet_name is not None:
            self.apifacet_name = apifacet_name
            self.api_base_url = context.apiurls[apifacet_name] + context.endpoints[apifacet_name][endpoint_name]

    def _send(self, method: str):

        if method == 'GET':
            pass
            self.response = requests.get(self.api_base_url, params=self.params, headers=self.headers)
        elif method == 'POST':
            self.response = requests.post(self.api_base_url, headers=self.headers, data=self.payload, params=self.params)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')
        print(self.response.status_code)

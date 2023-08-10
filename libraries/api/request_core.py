import requests

from libraries.api.api_sanitizer import RequestProps


class Requests(RequestProps):
    def __init__(self, context=None, apifacet_name=None, endpoint_name=None):
        super().__init__()
        self.response_dict = {}
        if apifacet_name is not None:
            self.apifacet_name = apifacet_name
            if endpoint_name:
                self.api_base_url = context.apiurls[apifacet_name] + context.endpoints[apifacet_name][endpoint_name]
            else:
                self.api_base_url = context.apiurls[apifacet_name]

    def _send(self, method: str):

        try:
            if method == 'GET':
                pass
                self.response = requests.get(self.api_base_url, params=self._params, headers=self.headers, verify=False)
            elif method == 'POST':
                self.response = requests.post(self.api_base_url, headers=self.headers, data=self.payload, params=self._params, verify=False)
            else:
                raise Exception(f'Invalid HTTP method "{method}" was received')
            print(self.response.status_code)
            # This will help us pick up anything from the Response of a request.
            self.response_dict['code'] = self.response.status_code
            self.response_dict['headers'] = self.response.headers
            self.response_dict['content'] = self.response.content
            self.response_dict['text'] = self.response.text
            self.response_dict['cookies'] = self.response.cookies
            self.response_dict['redirect'] = self.response.is_redirect


        except requests.RequestException as e:
            print(f'Method: {method} \n API URL {self.api_base_url} \n Params {self._params} \n Headers {self.headers} \n')
            print(f'Exception {e}')
        except Exception as e:
            print(f'Method: {method} \n API URL {self.api_base_url} \n Params {self._params} \n Headers {self.headers} \n')
            print(f'Exception {e}')
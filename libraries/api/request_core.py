import requests

from libraries.api.api_sanitizer import RequestProps
from project_runner import logger


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

    def validate_response_is_json(self, response):
        try:
            response.json()
            return True
        except Exception as e:
            logger.info("Response invalid json")
            return False

    def _send(self, method: str):
        try:
            self.response = requests.request(method=method, url=self.api_base_url, headers=self.headers, data=self.payload, params=self.params,
                                             verify=False)
            # This will help us pick up anything from the Response of a request.
            if self.validate_response_is_json(self.response):
                self.response_dict['json'] = self.response.json()
            self.response_dict['code'] = self.response.status_code
            self.response_dict['headers'] = self.response.headers
            self.response_dict['content'] = self.response.content
            self.response_dict['text'] = self.response.text
            self.response_dict['cookies'] = self.response.cookies
            self.response_dict['redirect'] = self.response.is_redirect
            logger.info(self.response_dict['content'])
        except requests.RequestException as e:
            logger.error(f'Method: {method} \n API URL {self.api_base_url} \n Params {self.params} \n Headers {self.headers} \n')
            logger.info(f'Exception {e}')
            assert False, f'Method: {method} \n API URL {self.api_base_url} \n Params {self.params} \n Headers {self.headers} \n'
        except Exception as e:
            logger.error(f'Method: {method} \n API URL {self.api_base_url} \n Params {self.params} \n Headers {self.headers} \n')
            logger.info(f'Exception {e}')
            assert False, f'Method: {method} \n API URL {self.api_base_url} \n Params {self.params} \n Headers {self.headers} \n'
        except:
            raise Exception(f'Invalid HTTP method "{method}" was received')

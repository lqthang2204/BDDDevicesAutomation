import requests


class Requests:

    @staticmethod
    def __init__(context, apifacet_name, endpoint_name):
        Requests.apifacet_name = apifacet_name
        Requests.api_base_url = context.apiurls[apifacet_name] + context.endpoints[apifacet_name][endpoint_name]
        Requests.response = None
        Requests.data = None
        Requests.payload = None
        Requests.headers = None
        Requests.cookies = None

    @staticmethod
    def _send( method: str):
        if method == 'GET':
            Requests.response = requests.get(Requests.api_base_url, params=Requests.data, headers=Requests.headers, cookies=Requests.cookies)
        elif method == 'POST':
            Requests.response = requests.post(Requests.api_base_url, data=Requests.payload, headers=Requests.headers, cookies=Requests.cookies)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')

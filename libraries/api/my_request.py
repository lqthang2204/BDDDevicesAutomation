import json

import requests

from libraries.api.api_sanitizer import RequestProps


class Requests(RequestProps):
    req_props = None
    @staticmethod
    def __init__(context, apifacet_name, endpoint_name):
        Requests.apifacet_name = apifacet_name
        Requests.api_base_url = context.apiurls[apifacet_name] + context.endpoints[apifacet_name][endpoint_name]
        Requests.req_props = RequestProps()
        Requests.cookies = {}
        Requests.payload = {}

    @staticmethod
    def _send( method: str, table):
        if table:
            list_data = []
            for row in table:
                if row['FieldName'] == 'params':
                    list_data.append(row['fieldValue'])
            Requests.para = json.dumps(list_data)
        if method == 'GET':
            Requests.response = requests.get(Requests.api_base_url, params=Requests.para, headers=Requests.req_props.headers, cookies=Requests.cookies)
        elif method == 'POST':
            Requests.response = requests.post(Requests.api_base_url,  headers=Requests.req_props.headers, cookies=Requests.cookies, json=Requests.req_props.payload)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')
        print(Requests.response.status_code)

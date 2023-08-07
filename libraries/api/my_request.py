import json

import requests


class Requests:

    @staticmethod
    def __init__(context, apifacet_name, endpoint_name):
        Requests.apifacet_name = apifacet_name
        Requests.api_base_url = context.apiurls[apifacet_name] + context.endpoints[apifacet_name][endpoint_name]
        Requests.response = None
        Requests.para = None
        Requests.payload = None
        Requests.headers = None
        Requests.cookies = None
        Requests.body = None

    @staticmethod
    def _send( method: str, table):
        if table:
            list_data = []
            for row in table:
                if row['FieldName'] == 'params':
                    list_data.append(row['fieldValue'])
            Requests.para = json.dumps(list_data)
        if method == 'GET':
            Requests.response = requests.get(Requests.api_base_url, params=Requests.para, headers=Requests.headers, cookies=Requests.cookies)
        elif method == 'POST':
            Requests.response = requests.post(Requests.api_base_url, data=Requests.para, headers=Requests.headers, cookies=Requests.cookies, json=Requests.body)
        else:
            raise Exception(f'Bad HTTP method "{method}" was received')

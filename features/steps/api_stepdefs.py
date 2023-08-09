import json
import os

from behave import *

from libraries.api.api_asserts import APIAsserts
from libraries.api.request_core import Requests
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable

req = None

@step(u'I set apifacet as {api_facet} for endpoint {endpoint_name}')
def step_impl(context, api_facet, endpoint_name):
    global req
    req = Requests(context, api_facet, endpoint_name)


@step(u'I set headers with below attributes')
def step_impl(context):
    global req
    headers = {}
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            result = get_test_data_for(row[1], context.dict_save_value)
            headers[row[0]] = result
    req.headers = headers


# Required Step RegEx for all
# @step(u'I set payload {payload_file}(?: with below attributes|$)')
# so that if it has with below attributes only then we read the Datatable else not
@step(u'I set payload {payload_file} with below attributes')
def step_impl(context, payload_file):
    global req
    payload_file = os.path.join(context.root_path, 'resources', 'api', 'request-json', payload_file + '.json')
    print(f'payload file : {payload_file}')
    with open(payload_file, 'r') as file:
        payload_json = file.read()
    # After reading We can read the Datatable and replace the values with some Runtime values also using the function get_test_data_for()
    payload_json = payload_json.replace('\n', '')
    req.payload = payload_json


@step(u'I trigger {api_method} call with below attributes')
def step_impl(context, api_method):
    global req

    # Below code to be re-written moved into a separate function as it will include a lot of detailing based on Issue #30
    if context.table:
        context_table = sanitize_datatable(context.table)
        list_data = []
        for row in context_table:
            if row[0] == 'params':
                list_data.append(row['fieldValue'])
        req.params = json.dumps(list_data)
    #  code to be moved into a separate function as it will include a lot of detailing based on Issue #30

    req._send(api_method)


@step(u'I verify the response with below attributes')
def step_impl(context):
    global req
    # Assert.response_has_key(Requests.response, context.table)
    APIAsserts.response_has_key(req.response, context.table)

import json
import os

from behave import *

from libraries.api.api_asserts import APIAsserts
from libraries.api.request_core import Requests
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable


@step(u'I set apifacet as {api_facet} for endpoint {endpoint_name}')
def step_impl(context, api_facet, endpoint_name):
    context.req = Requests(context, api_facet, endpoint_name)


@given(u'I set apifacet {api_facet} without endpoint')
def step_impl(context, api_facet):
    context.req = Requests(context, api_facet)


@step(u'I set headers with below attributes')
def step_impl(context):
    headers = {}
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            result = get_test_data_for(row[1], context.dict_save_value)
            headers[row[0]] = result
    context.req.headers = headers


# Required Step RegEx for all
# @step(u'I set payload {payload_file}(?: with below attributes|$)')
# so that if it has with below attributes only then we read the Datatable else not
@step(u'I set payload {payload_file} with below attributes')
def step_impl(context, payload_file):
    payload_file = os.path.join(context.root_path, 'resources', 'api', 'request-json', payload_file + '.json')
    print(f'payload file : {payload_file}')
    with open(payload_file, 'r') as file:
        payload_json = file.read()
    # After reading We can read the Datatable and replace the values with some Runtime values also using the function get_test_data_for()
    payload_json = payload_json.replace('\n', '')
    context.req.payload = payload_json


@step(u'I trigger {api_method} call with below attributes')
def step_impl(context, api_method):
    # Below code to be re-written moved into a separate function as it will include a lot of detailing based on Issue #30
    if context.table:
        context_table = sanitize_datatable(context.table)
        list_data = []
        for row in context_table:
            list_data.append(row[0])
        if list_data:
            context.req.params = json.dumps(list_data)
    #  code to be moved into a separate function as it will include a lot of detailing based on Issue #30
    context.req._send(api_method)


@step(u'I verify response body with below attributes')
def step_impl(context):
    APIAsserts.response_has_key(context.req.response_dict, context.table, "", "body")


@step(u'I verify response header with below attributes')
def step_impl(context):
    APIAsserts.response_has_key(context.req.response_dict, context.table, "", "header")


@step(u'I verify response code with status is "{status_code}"')
def step_impl(context, status_code):
    APIAsserts.response_has_key(context.req.response_dict, context.table, status_code, "response_code")

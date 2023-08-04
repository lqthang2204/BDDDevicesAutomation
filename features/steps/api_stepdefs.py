import os

from behave import *

from libraries.api.my_request import Requests
from libraries.api.api_asserts import APIAsserts as Assert
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable


@step(u'I set apifacet as {api_facet} for endpoint {endpoint_name}')
def step_impl(context, api_facet, endpoint_name):
    Requests(context, api_facet, endpoint_name)


@step(u'I set headers with below attributes')
def step_impl(context):
    headers = {}
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            result = get_test_data_for(row[1], context.dict_save_value)
            headers[row[0]] = result
    Requests.headers = headers


# Required Step RegEx for all
# @step(u'I set payload {payload_file}(?: with below attributes|$)')
# so that if it has with below attributes only then we read the Datatable else not
@step(u'I set payload {payload_file} with below attributes')
def step_impl(context, payload_file):
    payload_file = os.path.join(context.project_folder, 'resources', 'api', 'request-json', payload_file + '.json')
    with open(payload_file, 'r') as file:
        payload_json = file.read()
    # After reading We can read the Datatable and replace the values with some Runtime values also using the function get_test_data_for()
    Requests.payload = payload_json


@step(u'I trigger {api_method} call with below attributes')
def step_impl(context, api_method):
    if api_method == 'POST':
        Requests._send(api_method)


@step(u'I verify the response with below attributes')
def step_impl(context):
    Assert.status_code(Requests.response, 200)
import json
import os

from behave import *

from libraries.api.api_asserts import APIAsserts
from libraries.api.request_core import Requests
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable
from project_runner import logger
from libraries.api import api_newman


@step(u'I set apifacet as {api_facet} for endpoint {endpoint_name}')
def step_impl(context, api_facet, endpoint_name):
    context.req = Requests(context, api_facet, endpoint_name)


@given(u'I set apifacet as {api_facet} without endpoint')
def step_impl(context, api_facet):
    context.req = Requests(context, api_facet)


@step(u'I set headers with below attributes')
def step_impl(context):
    headers = {}
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            result = get_test_data_for(row[1], context.dict_save_value)
            if row[0] == 'Authorization':
                result = 'Bearer ' + result
            headers[row[0]] = result
    context.req.headers = headers


# Required Step RegEx for all
# @step(u'I set payload {payload_file}(?: with below attributes|$)')
# so that if it has with below attributes only then we read the Datatable else not
@step(u'I set payload {payload_file} with below attributes')
def step_impl(context, payload_file):
    payload_file = os.path.join(context.root_path, 'resources', 'api', 'request-json', payload_file + '.json')
    logger.info(f'payload file : {payload_file}')
    with open(payload_file, 'r') as file:
        payload_json = file.read()
    # After reading We can read the Datatable and replace the values with some Runtime values also using the function get_test_data_for()
    payload_json = json.loads(payload_json)
    context.req.set_payload(payload_json, context)


@step(u'I set payload {payload_file}')
def step_impl(context, payload_file):
    if context.table:
        logger.error(
            'you are setting below attributes with datatable but it is not required, please choise script "set payload {payload_file} with below attributes"')
    else:
        payload_file = os.path.join(context.root_path, 'resources', 'api', 'request-json', payload_file + '.json')
        logger.info(f'payload file : {payload_file}')
        with open(payload_file, 'r') as file:
            payload_json = file.read()
        # After reading We can read the Datatable and replace the values with some Runtime values also using the function get_test_data_for()
        payload_json = json.loads(payload_json)
        context.req.set_payload(payload_json, context)


@step(u'I set form {payload_file} with below attributes')
def step_impl(context, payload_file):
    payload_file = os.path.join(context.root_path, 'resources', 'api', 'request-json', payload_file + '.json')
    logger.info(f'payload file : {payload_file}')
    with open(payload_file, 'r') as file:
        payload_json = file.read()
    context.req.payload = json.loads(payload_json)


@step(u'I trigger {api_method} call request with below attributes')
def step_impl(context, api_method):
    # Below code to be re-written moved into a separate function as it will include a lot of detailing based on Issue #30
    if context.table:
        context_table = sanitize_datatable(context.table)
        list_data = []
        for row in context_table:
            if row[0].lower() == 'param':
                list_data.append(row[1])
            elif row[0].lower() == 'path':
                context.req.api_base_url = context.req.api_base_url.replace('{' + row[1] + '}',
                                                                            get_test_data_for(row[2],
                                                                                              context.dict_save_value))
        if list_data:
            context.req.params = json.dumps(list_data)
    #  code to be moved into a separate function as it will include a lot of detailing based on Issue #30
    context.req._send(api_method)


# @step(u'I verify response {body} with below attributes')
# def step_impl(context, response):
#     APIAsserts.response_has_key(context.req.response_dict, context, context.table, "", response)

@step(u'I trigger {api_method} call request')
def step_impl(context, api_method):
    context.req._send(api_method)


@step(u'I verify response {response} with below attributes')
def step_impl(context, response):
    APIAsserts.response_has_key(context.req.response_dict, context, context.table, "", response)


@step(u'I verify response {code} with status is "{status_code}"')
def step_impl(context, status_code, code):
    APIAsserts.response_has_key(context.req.response_dict, context, context.table, status_code, code)


@given(u'I poll the {api_method} call "{times_number}" times until below conditions')
def step_impl(context, api_method, times_number):
    context_table = sanitize_datatable(context.table)
    success = False
    for i in range(int(times_number)):
        context.req._send(api_method)
        for row in context_table:
            try:
                if row[0] == 'response_code':
                    APIAsserts.response_has_key(context.req.response_dict, context, context.table, row[1],
                                                "code")
                else:
                    APIAsserts.response_has_key(context.req.response_dict, context, context.table, "", "body")
                success = True
            except AssertionError:
                success = False
                continue

        if success:
            break
    if not success:
        raise Exception('Polling attempts exceeded')

@step(u'I run postman collection file {} with data file {} with override value')
def step_impl(context, collection_json_file, data_file):
    import datetime
    if context.table:
        collection_path = os.path.join(context.root_path, "resources/postman-test/collection",
                                       f"{collection_json_file}")
        data_file_path = os.path.join(context.root_path, "resources/postman-test/data-file", f"{data_file}")
        try:
            os.makedirs(os.path.dirname(collection_path), exist_ok=True)
            os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            logger.error(f"Error: The file '{file_path}' was not found.")
            raise FileNotFoundError
        context_table = sanitize_datatable(context.table)
        data = api_newman.update_data(data_file_path, context_table, dict_save_value=context.dict_save_value)
        current_time = datetime.datetime.now()
        date_time = str(current_time.year) + '_' + str(current_time.month) + '_' + str(current_time.day) + '_' + str(
            current_time.microsecond)
        new_data_file = os.path.join(context.root_path, "resources/postman-test/data-file", f"data_collection_{date_time}.json")
        if api_newman.write_file_data(data, new_data_file):
            api_newman.run_command(collection_path, new_data_file)
            api_newman.delete_file_data(new_data_file)

        # for row in context_table:
        #     logger.info(row)


    print("test ")
@step(u'I run postman collection file {} with data file {}')
def step_impl(context, collection_json_file, data_file):
    collection_path = os.path.join(context.root_path, "resources/postman-test/collection", f"{collection_json_file}")
    data_file_path = os.path.join(context.root_path, "resources/postman-test/data-file", f"{data_file}")
    try:
        os.makedirs(os.path.dirname(collection_path), exist_ok=True)
        os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        logger.error(f"Error: The file '{file_path}' was not found.")
        raise FileNotFoundError
    api_newman.run_command(collection_path, data_file_path)
@step(u'I run postman collection file {}')
def step_impl(context, collection_json_file):
    file_path = os.path.join(context.root_path, "resources/postman-test/collection", f"{collection_json_file}")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        logger.error(f"Error: The file '{file_path}' was not found.")
        raise FileNotFoundError
    api_newman.run_command(file_path)



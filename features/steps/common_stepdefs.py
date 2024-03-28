from time import sleep

from behave import *

from Utilities.common_ui import common_device
from libraries.accessibility_report import perform_accessibility_verification
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable
from libraries.number_string_operations import check_and_call_operator
from project_runner import logger
from execute_open_browser import manage_hook_browser


@step(u'I create a set of keys with below attributes')
def step_impl(context):
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            result = get_test_data_for(row[0], context.dict_save_value)
            # for DEBUG
            # print(f'{row[0].ljust(40)} {row[1].ljust(30)} {result}')

            # saving the value to context
            context.dict_save_value['KEY.' + row[1]] = result

    return context.dict_save_value


@step(u'I run accessibilty test on {page_name}')
def run_accessibility(context, page_name):
    perform_accessibility_verification(context.driver, page_name)


@step(u'I perform operations with below attributes')
def step_impl(context):
    if context.table:
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            operator_func = check_and_call_operator(row[1])
            if operator_func is not None:
                left_data = get_test_data_for(row[0], context.dict_save_value)
                right_data = get_test_data_for(row[2], context.dict_save_value)
                result = operator_func(left_data, right_data)
                if not result:
                    to_display_left, to_display_right = [(' as ' + left_data) if left_data != row[0] else '',
                                                         (' as ' + right_data) if right_data != row[2] else '']
                    raise AssertionError(f'Failing condition: {row[0]}{to_display_left} {row[1]} {row[2]}{to_display_right}')
                else:
                    logger.info(f'Success: {row[0]} {row[1]} {row[2]}')
                # saving the value to context
                if row[3]:
                    if row[3].startswith('KEY.'):
                        new_key_name = row[3]
                    else:
                        new_key_name = 'KEY.' + row[3]
                    context.dict_save_value[new_key_name] = result
            else:
                raise NotImplementedError(f'{row[1]}: is not a recognized operator')

    return context.dict_save_value


# Only for DEBUG purpose when you want to pring all the key-Values
@step(u'I print all the dictionary keys')
def step_impl(context):
    logger.info('------ Displaying Dictionary keys ------')
    for keys, value in context.dict_save_value.items():
        logger.info(f'{keys}, {value}')


@step(u'I wait {wait_duration} seconds')
def step_impl(context, wait_duration):
    logger.info(f'waiting for {wait_duration} seconds')
    sleep(int(wait_duration))
@step(u'I navigate to url {name} with options below')
def navigate_with_option(context, name):
    if context.table:
        context_table = sanitize_datatable(context.table)
        manage_hook_browser().open_browser(context, context_table, name)
@step(u'I perform javascript {file} with below arguments')
def step_impl(context, file):
    if context.table:
        print("test")
        context_table = sanitize_datatable(context.table)
        for row in context_table:
            arr_args = []
            for value in row[0].split(","):
                element = common_device().get_element(context.page_present, value.strip(),
                                                      context.device['platformName'], context.dict_save_value)
                arr_args.append(element)
                print("arr_args ", arr_args)
            common_device().execute_javascript_with_table(context.root_path, arr_args, file, context.driver,
                                                        context.device)

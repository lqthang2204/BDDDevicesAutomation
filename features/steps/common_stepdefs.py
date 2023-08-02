import logging
from time import sleep

from behave import *

from Utilities.accessibility_report import perform_accessibility_verification
from libraries.data_generators import get_test_data_for
from libraries.misc_operations import sanitize_datatable
from libraries.number_string_operations import check_and_call_operator


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
                    logging.info(f'Success: {row[0]} {row[1]} {row[2]}')
                # saving the value to context
                if row[3]:
                    context.dict_save_value['KEY.' + row[3]] = result
            else:
                raise NotImplementedError(f'{row[1]}: is not a recognized operator')

    return context.dict_save_value


# Only for DEBUG purpose when you want to pring all the key-Values
@step(u'I print all the dictionary keys')
def step_impl(context):
    print('------ Displaying Dictionary keys ------')
    for keys, value in context.dict_save_value.items():
        print(keys, value)
    print('------ Printed Dictionary keys ------')


@step(u'I wait {wait_duration} seconds')
def step_impl(context, wait_duration):
    logging.info(f'waiting for {wait_duration} seconds')
    sleep(int(wait_duration))

from time import sleep

from behave import *

from libraries.random_generators import when_sample_data_contains_reserved_symbol


@step(u'I create a set of keys with below attributes')
def step_impl(context):
    if context.table:
        for row in context.table:
            result = when_sample_data_contains_reserved_symbol(row[0])
            print(f'{row[0].ljust(40)} {row[1].ljust(30)} {result}')
            # saving the value to context
            context.dict_save_value['KEY.' + row[1]] = result

    return context.dict_save_value


# Only for Debugging purpose when you want to pring all the key-Values
@step(u'I print all the dictionary keys')
def step_impl(context):
    print('------ Displaying Dictionary keys ------')
    for keys, value in context.dict_save_value.items():
        print(keys, value)
    print('------ Printed Dictionary keys ------')


@step(u'I wait {wait_duration} seconds')
def step_impl(context, wait_duration):
    print(f'waiting for {wait_duration} seconds')
    sleep(wait_duration)

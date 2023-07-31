numerical_comparison = {
    'greater-than': lambda x, y: float(x) > float(y) + 1e-9,
    'greater-than-equal-to': lambda x, y: float(x) >= float(y) - 1e-9,
    'less-than': lambda x, y: float(x) < float(y) - 1e-9,
    'less-than-equal-to': lambda x, y: float(x) <= float(y) + 1e-9,
    'equal-to': lambda x, y: abs(float(x) - float(y)) < 1e-9,  # Floating-point tolerance
    'not-equal-to': lambda x, y: abs(float(x) - float(y)) >= 1e-9,  # Floating-point tolerance
}

string_comparison = {
    'contains': lambda x, y: y in x,
    'case-match': lambda x, y: x == y,
    'ignore-case': lambda x, y: x.lower() == y.lower(),
    'does-not-match': lambda x, y: x != y,

}

other_operations = {
    'add': lambda x, y: float(x) + float(y),
    'subtract': lambda x, y: float(x) - float(y),
    'multiply': lambda x, y: float(x) * float(y),
    'divide': lambda x, y: float(x) / float(y),
    'concat' or 'concatenate': lambda x, y: x + y
}


def numerical_comparison_by_operator(operator, number_left, number_right):
    comparison_func = numerical_comparison.get(operator)
    assert comparison_func(number_left, number_right)


def string_comparison_by_operator(operator, string_left, string_right):
    comparison_func = string_comparison.get(operator)
    assert comparison_func(string_left, string_right)


def calculate_value_by_operator(operator, number_left, number_right):
    calc_func = other_operations.get(operator)
    assert calc_func(number_left, number_right)


def check_and_call_operator(key_to_check):
    if key_to_check in numerical_comparison:
        return numerical_comparison[key_to_check]
    elif key_to_check in string_comparison:
        return string_comparison[key_to_check]
    elif key_to_check in other_operations:
        return other_operations[key_to_check]
    else:
        return None


if __name__ == '__main__':
    key_to_check = 'greater-than'
    operator_func = check_and_call_operator(key_to_check)
    if operator_func is not None:
        result = operator_func(5.0, 3.0)
        print(result)

    key_to_check = 'contains'
    operator_func = check_and_call_operator(key_to_check)
    if operator_func is not None:
        result = operator_func('hello', 'oell')
        print(result)

    key_to_check = 'concat'
    operator_func = check_and_call_operator(key_to_check)
    if operator_func is not None:
        result = operator_func('hello_', ' user')
        print(result)

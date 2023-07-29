import logging


def numerical_comparison_by_operator(operator, number_left, number_right):
    try:
        if operator == "greater-than":
            assert number_left > number_right
        elif operator == "greater-than-equal-to":
            assert number_left >= number_right
        elif operator == "less-than":
            assert number_left < number_right
        elif operator == "less-than-equal-to":
            assert number_left <= number_right
        elif operator == "equal-to":
            assert abs(number_left - number_right) < 1e-9  # Floating-point tolerance
        elif operator == "not-equal-to":
            assert abs(number_left - number_right) >= 1e-9  # Floating-point tolerance
        else:
            assert abs(number_left - number_right) < 1e-9  # Floating-point tolerance (default)
    except AssertionError as e:
        logging.error(f"Failing condition: {number_left} {operator} {number_right}")
        raise e


def string_comparison_by_operator(operator, string_left, string_right):
    try:
        if operator == "contains":
            assert string_left.find(string_right) != -1
        elif operator == "case-match":
            assert string_left == string_right
        elif operator == "ignore-case":
            assert string_left.lower() == string_right.lower()
        elif operator == "does-not-match":
            assert string_left != string_right
        else:
            logging.error("Un-implemented switch-case in string_comparison_by_operator")
            raise AssertionError("Invalid operator")
    except AssertionError as e:
        raise e


def calculate_value(value1, operator, value2):
    operator = operator.lower()
    if operator == "add":
        return value1 + value2
    elif operator == "subtract":
        return value1 - value2
    elif operator == "divide":
        return value1 / value2
    elif operator == "multiply":
        return value1 * value2
    else:
        logging.info("The following operator is invalid: %s", operator)
        return 0.0


if __name__ == '__main__':
    # Sample usage of the functions
    numerical_comparison_by_operator("greater-than", 5.0, 3.0)
    string_comparison_by_operator("contains", "hello", "ell")
    print(calculate_value(5.0, "add", 3.0))

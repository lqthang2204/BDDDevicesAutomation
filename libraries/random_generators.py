import random
import re
from datetime import datetime, timedelta
from pytz import timezone, UTC

ALPHANUMERIC = 'alphanumeric_'
NUMBERPREFIX = 'number_'
ALPHABETPREFIX = 'alphabet_'

format_mapping = {
    'yyyy': '%Y',
    'MM': '%m',
    'dd': '%d',
    'hh': '%H',
    'mm': '%M',
    'ss': '%S',
    'zzz': '%z'  # Adjusted the format specifier for timezone offset
}


def when_sample_data_contains_dollar_symbol(sample_data):
    ret_string = None
    if sample_data is not None:
        if sample_data.startswith('random_'):
            ret_string = generate_random_numeric_alpha_string(sample_data)
        elif sample_data.startswith('date') or sample_data.startswith('time'):
            ret_string = generate_date_time_zone(sample_data)
    return ret_string


def generate_random_numeric_alpha_string(value):
    result = None
    value = value.replace('random_', '')
    if '.' in value:
        value = value.replace(NUMBERPREFIX, '')
        if '-' in value:
            min_int, max_int = map(int, value.split('.')[0].split('-'))
            min_decimal, max_decimal = map(int, value.split('.')[1].split('-'))
            result = str(get_random_number_in_decimal(min_int, max_int, min_decimal, max_decimal))
        else:
            max_int, min_decimal = map(int, value.split('.'))
            result = f'{get_random_number(max_int)}.{get_random_number(min_decimal)}'
    elif 'email' in value:
        result = f'AutoGenEmail_{get_random_alphanumeric(20)}@Test.com'
    else:
        if '-' in value:
            result = for_rand_string_when_value_contains_hyphen(value)
        else:
            result = for_rand_string_when_value_contains_else(value)

    return result


def get_random_number_in_decimal(min_int, max_int, min_deci, max_deci):
    result_int = get_random_number_in_range(min_int, max_int)
    result_decimal = get_random_number_in_range(min_deci, max_deci)
    length_decimal = len(str(result_decimal))
    return result_int + result_decimal / 10 ** length_decimal


def get_random_number(random_int_length):
    return ''.join(random.choices('0123456789', k=random_int_length))


def get_random_number_in_range(min_num, max_num):
    return random.randint(min_num, max_num)


def for_rand_string_when_value_contains_hyphen(value):
    result = ''
    if ALPHABETPREFIX in value:
        value = value.replace(ALPHABETPREFIX, '')
        min_int, max_int = map(int, value.split('-'))
        result = get_random_alphabetic_in_range(min_int, max_int)
    elif ALPHANUMERIC in value:
        value = value.replace(ALPHANUMERIC, '')
        min_int, max_int = map(int, value.split('-'))
        result = get_random_alphanumeric_in_range(min_int, max_int)
    elif NUMBERPREFIX in value:
        value = value.replace(NUMBERPREFIX, '')
        min_int, max_int = map(int, value.split('-'))
        result = str(get_random_number_in_range(min_int, max_int))
    return result


def get_random_alphanumeric(random_str_length):
    return ''.join(
        random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random_str_length))


def date_accessor_mapper(user_format):
    if user_format:
        for key, value in format_mapping.items():
            user_format = user_format.replace(key, value)
    return user_format


def find_value_with_pattern(text, regex):
    match = re.search(regex, text)
    if match:
        return match.group(0)
    return None


def verify_text_using_regex(text_value, regex_pattern):
    return bool(re.search(regex_pattern, text_value))


def add_years(dt, years):
    try:
        return dt.replace(year=dt.year + years)
    except ValueError:
        # February 29 may become non-existent after adding years (e.g., 2020 + 1 = 2021)
        # In that case, set the date to February 28 of the target year
        return dt.replace(year=dt.year + years, day=28)


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1

    try:
        return dt.replace(year=year, month=month)
    except ValueError:
        # If the resulting month is February and the day is 29 (leap year),
        # set the date to February 28
        return dt.replace(year=year, month=month, day=28)


def get_desired_date_time(property_str):
    now = datetime.now()

    if "current" in property_str:
        return now

    value = int(find_value_with_pattern(property_str, r"[+-]\d*"))

    if verify_text_using_regex(property_str, r"[+-]\d*ms"):
        return now + timedelta(milliseconds=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*mi"):
        return now + timedelta(minutes=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*mo"):
        return add_months(now, value)
    elif verify_text_using_regex(property_str, r"[+-]\d*hr"):
        return now + timedelta(hours=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*sc"):
        return now + timedelta(seconds=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*wk"):
        return now + timedelta(weeks=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*dt"):
        return now + timedelta(days=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*yr"):
        return add_years(now, value)

    return now


def generate_date_time_zone(value):
    result = ''
    req_date_formatter = None
    now = get_desired_date_time(value)
    split_format = value.split('_')
    if len(split_format) == 3 and (
            verify_text_using_regex(split_format[2], r'[-/][dMy]') or verify_text_using_regex(split_format[2],
                                                                                              r'[-/:][hms]')):
        req_date_formatter = date_accessor_mapper(split_format[2])

    if 'dateTime_' in value:
        result = get_result_value(now, value)
    elif 'year' in value or 'dayOfWeek' in value:
        result = when_req_is_year_or_day_of_week(value, now)
    elif 'date_' in value:
        if req_date_formatter:
            result = now.strftime(req_date_formatter)
        else:
            result = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            if 'yyymmdd' in value:
                result = now.strftime('%Y%m%d')
    elif 'time_' in value:
        if req_date_formatter:
            result = now.strftime(req_date_formatter)
        else:
            result = now.strftime('%H:%M:%S')
    return result


def get_result_value(now, value):
    result = ''
    ret_matcher = re.search(r'(_[\dZ])', value)
    if ret_matcher:
        ret_matcher = ret_matcher.group(1).replace('_', '')
        digits = int(ret_matcher)
        result = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:digits + 1] + 'Z' if digits > 0 else now.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        result = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return result


def when_req_is_year_or_day_of_week(value, now):
    result = ''
    if 'year' in value:
        result = str(now.year)
    elif 'dayOfWeek' in value:
        day_of_week = (now.weekday() + 1) % 5
        if day_of_week == 0:
            result = 'FRIDAY'
        else:
            result = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'][day_of_week - 1]
    return result


def get_random_alphabetic(random_str_length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random_str_length))


def for_rand_string_when_value_contains_else(value):
    result = ''
    if ALPHABETPREFIX in value:
        value = value.replace(ALPHABETPREFIX, '')
        result = get_random_alphabetic(int(value))
    elif ALPHANUMERIC in value:
        value = value.replace(ALPHANUMERIC, '')
        result = get_random_alphanumeric(int(value))
    elif NUMBERPREFIX in value:
        value = value.replace(NUMBERPREFIX, '')
        result = get_random_number(int(value))
    return result


def get_random_alphabetic_in_range(min_num, max_num):
    random_str_length = get_random_number_in_range(min_num, max_num)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random_str_length))


def get_random_alphanumeric_in_range(min_num, max_num):
    random_str_length = get_random_number_in_range(min_num, max_num)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                  k=random_str_length))


# Example Usage:
if __name__ == '__main__':
    formats = [
        'date_current_yyyy-MM-dd',
        'date_+3dt_yyyy-MM-dd',
        'date_+3dt_yyyy/MM/dd',
        'date_+3dt_dd/MM/yyyy',
        'date_+3dt_yyyy/dd/MM/',
        'dateTime_current',
        'dateTime_current',
        'dateTime_+1yr_UTC',
        'dateTime_+1mo_UTC',
        'dateTime_+1wk_UTC',
        'dateTime_+1800sc_UTC',
        'dateTime_-30mi_UTC',
        'dateTime_-1dt',
        'dateTime_-1dt_UTC',
        'date_current',
        'date_current_UTC',
        'date_+1dt',
        'time_current',
        'time_+2hr',
        'time_-25mi',
        'time_current_hh:mm',
        'time_+2hr_hh:mm',
        'time_-25mi_hh:mm',
        'date_current_year',
        'date_+1yr_year',
        'date_+3dt_dayOfWeek',
        'date_current_dayOfWeek',
        'time_current_UTC',
        'random_alphabet_5',
        'random_alphabet_10',
        'random_alphabet_5-8',
        'random_alphanumeric_7',
        'random_alphanumeric_8-12',
        'random_number_3',
        'random_number_3-5',
        'random_number_3.random_number_2',
        'random_number_10-15.random_number_10-15'
    ]

    for format_str in formats:
        print(f"Given-Format: {format_str}    Output: {when_sample_data_contains_dollar_symbol(format_str)}")

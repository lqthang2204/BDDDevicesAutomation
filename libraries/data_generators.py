import random
import re
import uuid
from datetime import datetime, timedelta

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


def get_test_data_for(sample_data, context_dict):
    if sample_data is not None:
        if sample_data in ['EMPTY', 'BLANK']:
            return ''
        elif sample_data == 'NULL':
            return None
        elif sample_data == 'uuid':
            return get_uuid()
        elif sample_data.startswith('random_'):
            return generate_random_numeric_alpha_string(sample_data)
        elif sample_data.startswith('date') or sample_data.startswith('time'):
            return generate_date_time_zone(sample_data)
        else:
            if context_dict:
                if not sample_data.startswith('KEY.'):
                    srch_key = 'KEY.' + sample_data
                else:
                    srch_key = sample_data
                return str(context_dict.get(srch_key, sample_data))
            else:
                return sample_data
    # if this line return None is encountered it means we have condition umimplemented
    return None


def generate_random_numeric_alpha_string(value):
    value = value.replace('random_', '')
    if '.' in value:
        value = value.replace(NUMBERPREFIX, '')
        if '-' in value:
            min_int, max_int = map(int, value.split('.')[0].split('-'))
            min_decimal, max_decimal = map(int, value.split('.')[1].split('-'))
            return str(get_random_number_in_decimal(min_int, max_int, min_decimal, max_decimal))
        else:
            max_int, min_decimal = map(int, value.split('.'))
            return f'{get_random_number(max_int)}.{get_random_number(min_decimal)}'
    else:
        if '-' in value:
            return for_rand_string_when_value_contains_hyphen(value)
        else:
            return for_rand_string_when_value_contains_else(value)


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


def get_random_alphanumeric(random_str_length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random_str_length))


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
        return add_time_to_date(now, months=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*hr"):
        return now + timedelta(hours=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*sc"):
        return now + timedelta(seconds=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*wk"):
        return now + timedelta(weeks=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*dt"):
        return now + timedelta(days=value)
    elif verify_text_using_regex(property_str, r"[+-]\d*yr"):
        return add_time_to_date(now, years=value)

    return now


def add_time_to_date(dt, years=0, months=0):
    try:
        return dt.replace(year=dt.year + years, month=dt.month + months)
    except ValueError:
        # February 29 may become non-existent after adding years (e.g., 2020 + 1 = 2021)
        # In that case, set the date to February 28 of the target year
        return dt.replace(year=dt.year + years, month=dt.month + months, day=28)


def generate_date_time_zone(value):
    now = get_desired_date_time(value)
    req_date_formatter = None

    split_format = value.split('_')
    if len(split_format) == 3 and (
            verify_text_using_regex(split_format[2], r'[-/][dMy]') or verify_text_using_regex(split_format[2],
                                                                                              r'[-/:][hms]')):
        req_date_formatter = date_accessor_mapper(split_format[2])

    if 'dateTime_' in value:
        return get_result_value(now, value)
    elif 'year' in value or 'dayOfWeek' in value:
        return when_req_is_year_or_day_of_week(value, now)
    elif 'date_' in value:
        if req_date_formatter:
            return now.strftime(req_date_formatter)
        else:
            return now.strftime('%Y-%m-%dT%H:%M:%S.%fZ') if 'yyymmdd' not in value else now.strftime('%Y%m%d')
    elif 'time_' in value:
        if req_date_formatter:
            return now.strftime(req_date_formatter)
        else:
            return now.strftime('%H:%M:%S')
    return ''


def get_result_value(now, value):
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
    if 'year' in value:
        return str(now.year)
    elif 'dayOfWeek' in value:
        day_of_week = (now.weekday() + 1) % 5
        return 'FRIDAY' if day_of_week == 0 else ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'][day_of_week - 1]
    return ''


def get_random_alphabetic(random_str_length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random_str_length))


def get_random_alphabetic_in_range(min_num, max_num):
    random_str_length = get_random_number_in_range(min_num, max_num)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random_str_length))


def get_random_alphanumeric_in_range(min_num, max_num):
    random_str_length = get_random_number_in_range(min_num, max_num)
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                  k=random_str_length))


def get_uuid():
    # Generate a UUID
    uuid_value = uuid.uuid4()
    # Convert the UUID to a string and replace hyphens with empty strings
    formatted_value = str(uuid_value).replace('-', '')
    # Insert hyphens at specific positions to match your desired format
    uuid_value = f"{formatted_value[:4]}-{formatted_value[4:10]}-{formatted_value[10:14]}-{formatted_value[14:18]}-{formatted_value[18:24]}-{formatted_value[24:]}"
    return uuid_value


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
        print(f"Given-Format: {format_str}    Output: {get_test_data_for(format_str)}")

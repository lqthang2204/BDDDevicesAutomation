def get_user(list_user, key):
    if '.' in key:
        list_key = key.split('.')
        if list_key[0].isnumeric():
            user = list_user[(int(list_key[0]) - 1)]
            key = list_key[1]
        else:
            assert False, f'index of user must be integer {key}'
    else:
        user = list_user[0]
    if key == 'email':
        return user.email
    elif key == 'first_name':
        return user[key]
    elif key == 'last_name':
        return user[key]
    elif key == 'full_name':
        return user['first_name'] +' '+user['last_name']
    elif key == 'job':
        return user[key]
    elif key == 'address':
        return user[key]
    elif key == 'phone_number':
        return user[key]
    elif key == 'city':
        return user[key]
    elif key == 'state':
        return user[key]
    elif key == 'postcode':
        return user[key]
    elif key == 'prefix':
        return user[key]
    elif key == 'suffix':
        return user[key]
    else:
        assert False, f'user do not contain attribute {key}'


def save_user_to_dict(dict_save_value, user):
    if dict_save_value.get('USER.'):
        list_user = dict_save_value.get('USER.')
        list_user.append(user)
        dict_save_value['USER.'] = list_user
    else:
        list_user = []
        list_user.append(user)
        dict_save_value['USER.'] = list_user

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
    if key in ["email", "first_name", "last_name", "job", "address", "phone_number", "city", "state", "postcode", "prefix", "suffix"]:
        return user[key]
    elif key == "full_name":
        return user['first_name'] +' '+user['last_name']
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

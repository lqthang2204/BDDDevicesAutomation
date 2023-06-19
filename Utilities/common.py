
def check_att_is_exist(obj_action_elements, key):
    if obj_action_elements.get(key) is None:
        return None
    else:
        return obj_action_elements.get(key)
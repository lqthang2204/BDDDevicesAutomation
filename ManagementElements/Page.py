class Page:

    def __init__(self):
        self.list = []
        self.dict_action = {}

    def get_list_element(self):
        return self.list
    def get_dict(self):
        return self.dict_action
    def set_list_element(self, list):
        self.list.append(list)
    def set_dict_action(self, key, value):
        self.dict_action[key] = value




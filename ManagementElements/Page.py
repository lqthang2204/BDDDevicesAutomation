from ManagementElements import Elements, ActionTest
class Page:
    dict_action = dict[str, ActionTest]
    list_element = [Elements]
    def get_list_element(self):
        return self.list_element
    def get_dict(self):
        return self.dict_action
    def set_list_element(self, list):
        self.list_element = list
    def set_dict_action(self, dict):
        self.dict_action = dict




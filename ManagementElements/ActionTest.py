from ManagementElements.ActionElements import ActionElements


class ActionTest:
    list_action = [ActionElements]

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_description(self):
        return self.id

    def set_description(self, description):
        self.description = description

    def set_list_action(self, list_action):
        self.list_action = list_action

    def get_list_action(self):
        return self.list_action

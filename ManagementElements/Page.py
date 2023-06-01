from typing import Any, Dict, List
import Elements, ActionTest
class Page:
    actions: Dict[str, ActionTest]
    elements: List[Elements]
    def get_list_element(self):
        return self.elements
    def get_dict(self):
        return self.actions
    def set_list_element(self, list):
        self.elements = list
    def set_dict_action(self, dict):
        self.actions = dict




from typing import Any
from ManagementElements.Locator import Locator


class Elements:
    list_locator = [Locator]

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_list_locator(self):
        return self.list_locator

    def set_id(self, id):
        self.id = id

    def set_description(self, description):
        self.description = description

    def set_list_locator(self, list_locator):
        self.list_locator = list_locator

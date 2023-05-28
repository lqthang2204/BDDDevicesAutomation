from typing import Any


class Elements:
    def __int__(self, id, description, locator):
        self.id = id
        self.description = description
        self.locator = locator

    def get_id(self):
        return self.id
    def get_description(self):
        return self.description

    def get_locator(self):
        return self.locator
    def set_id(self, id):
        self.id = id

    def set_description(self,description):
        self.description = description

    def set_locator(self,locator):
        self.locator = locator





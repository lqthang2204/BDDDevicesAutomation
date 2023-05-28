class Locator:
    def __init__(self, device, value, type):
        self.device = device
        self.value = value
        self.type = type


    def set_device(self,device):
        self.device = device
    def set_value(self, value):
        self.value = value
    def set_type(self, type):
        self.type = type
    def get_device(self):
        return self.device
    def get_value(self):
        return self.value
    def get_type(self):
        return self.type

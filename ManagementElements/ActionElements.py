class ActionElements:
    def __int__(self, element, condition, timeout, inputType, infoType):
        self.element = element
        self.condition = condition
        self.timeout = timeout
        self.inputType = inputType
        self.infoType = infoType

    def get_element(self):
        return self.element
    def get_condition(self):
        return self.condition
    def get_timeout(self):
        return self.timeout
    def get_inputType(self):
        return self.inputType
    def get_infoType(self):
        return self.infoType
    def set_element(self, element):
        self.element = element
    def set_condition(self, condition):
        self.condition = condition
    def set_timeout(self,timeout):
        self.timeout = timeout
    def set_input_type(self,input_type):
        self.infoType = input_type
    def set_info_type(self, info_type):
        self.infoType = info_type




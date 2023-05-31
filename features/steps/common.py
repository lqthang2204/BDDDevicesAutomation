class common_test:

    dict_yaml = {}


    def get_dict_yaml(self):
        print("get common")
        print(self.dict_yaml)
        return self.dict_yaml

    def set_dict_yaml(self, dict_yaml):
        self.dict_yaml = dict_yaml
        self.get_dict_yaml()



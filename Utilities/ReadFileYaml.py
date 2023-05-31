import os
import pathlib
import sys
import glob
from pathlib import Path


class read_file_yaml:

    # def __init__(self):
    #     self.dict_yaml = None
    #     self.files = None

    def get_dict_path_yaml():
        file_path = os.getcwd().replace("Utilities","")+"\\resources\\pages\\*\\*.yaml"
        dict_yaml = {}
        files = glob.glob(file_path)
        for file in files:
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        # dict_yaml_path = dict(dict_yaml)
        return dict_yaml


# obj = read_file_yaml()
# dict_1 = obj.get_dict_path_yaml()
# print(dict_1)

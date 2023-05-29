import os
import sys
import glob
from pathlib import Path


class read_file_yaml:
    def __init__(self, dict_yaml):
       self.dict_yaml = dict_yaml

    def get_dict_path_yaml(self):
        print("reading path yaml")
        file_path = sys.path[1] + '/resources/pages/*/*.yaml'
        # Find all files with the .txt extension in the specified directory
        files = glob.glob(file_path)
        for file in files:
            path, file_name = os.path.split(file)
            self.dict_yaml[file_name] = path
        print(self.dict_yaml)
        return self.dict_yaml



dict_yaml = {}
obj = read_file_yaml(dict_yaml)
obj.get_dict_path_yaml()
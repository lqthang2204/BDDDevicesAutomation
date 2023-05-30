import os
import sys
import glob
from pathlib import Path


class read_file_yaml:

    def get_dict_path_yaml(self):
        dict_yaml = dict()
        print("reading path yaml")
        file_path = sys.path[1] + '/resources/pages/*/*.yaml'
        # Find all files with the .txt extension in the specified directory
        files = glob.glob(file_path)
        for file in files:
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        # print(dict_yaml.get("pageOrange.yaml"))
        return (dict_yaml)



obj = read_file_yaml()
obj.get_dict_path_yaml()
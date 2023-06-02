import os
import pathlib
import sys
import glob
from typing import Dict, Any, List
from pathlib import Path
import yaml
from yaml import SafeLoader
import json


class ManagementFile:
    def get_dict_path_yaml():
        file_path = os.getcwd().replace("Utilities","")+"\\resources\\pages\\*\\*.yaml"
        dict_yaml = {}
        files = glob.glob(file_path)
        for file in files:
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        # dict_yaml_path = dict(dict_yaml)
        return dict_yaml
    def read_yaml_file(path):
        with open(path) as page:
            print("read file")
            json_string = page.read()
            python_dict = yaml.load(json_string, Loader=SafeLoader)
            json_result = json.dumps(python_dict)
            # print(json_result)
            json_object = json.loads(json_result)
            print ("type of final_dictionary", json_object["elements"])
    def parse_yaml_file(yaml_string) -> Dict[Any, Any]:  # NEW CONCEPT: Any can be any type. Could be string, integer or anything
        print("parse")
        print(yaml.safe_load(yaml_string))
        return yaml.safe_load(yaml_string)
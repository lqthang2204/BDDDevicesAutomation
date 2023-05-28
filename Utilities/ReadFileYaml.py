import os
import sys
import glob
from pathlib import Path


class read_file_yaml:
    def get_dict_path_yaml():
        dict_yaml = {}
        file_path = sys.path[1] + '/resources/pages/*/*.yaml'
        # Find all files with the .txt extension in the specified directory
        files = glob.glob(file_path)
        # Print the names of the files found
        for file in files:
            path, file_name = os.path.split(file)
            dict_yaml[file_name] = path
        return dict_yaml



if __name__ == '__main__':
    # read_file_yaml.get_json_from_yaml("google.yaml")

    dict = read_file_yaml.get_dict_path_yaml()
    print(dict)
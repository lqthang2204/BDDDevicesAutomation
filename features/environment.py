from Utilities.ReadFileYaml import read_file_yaml
from steps.common import common_test
def before_all(context):
    print("----------------------Reading file config-----------------------------")
    dict_yaml = read_file_yaml.get_dict_path_yaml()
    obj = common_test()
    obj.set_dict_yaml(dict_yaml)
from Utilities.ReadFileYaml import read_file_yaml
def before_all(context):
    print("----------------------Reading file config-----------------------------")
    dict_yaml = read_file_yaml.get_dict_path_yaml()
    print(dict_yaml)
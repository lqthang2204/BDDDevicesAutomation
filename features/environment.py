from Utilities.ReadFileYaml import read_file_yaml
def before_all(context):
    print("before run")
    dict_yaml = dict()
    obj = read_file_yaml()
    dict_yaml = obj.get_dict_path_yaml()
    print(dict_yaml)
    print(dict_yaml.get("pageGoogle.yaml"))
    # print(dict_yaml.get("pageGoogle.yaml"))
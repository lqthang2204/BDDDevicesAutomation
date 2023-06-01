from Utilities.ReadFileYaml import ManagementFile
import configparser
from selenium import webdriver
def before_all(context):
    file = open("config.ini", 'r')
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read_file(file)
    if config.get("drivers_config", "auto_download_driver") == 'True':
        context.driver = webdriver.Chrome(executable_path=config.get("drivers_config", "driver_version"))
    else:
        context.driver = webdriver.Chrome()
    print("----------------------Reading file config-----------------------------")
    context.dict_yaml = ManagementFile.get_dict_path_yaml()
import yaml
import os
from yaml import SafeLoader
import json
from Configuration.configuration_env import environment
from Configuration.devices import devices
from Utilities.common import check_att_is_exist
from Configuration.stage import stage
class read_configuration:
    def read(self):
        config_file_path = os.path.dirname(os.path.dirname(__file__))+"/environments.yml"
        with open(config_file_path) as configs_env:
            config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
            json_result = json.dumps(config_file)
            json_object = json.loads(json_result)
            # print(json_object)
            arr_config = json_object["env"]
            list_env = []
            env = environment()
            for config in arr_config:
                stage_env = stage()
                stage_env.set_stage(config["stage"])
                stage_env.set_link(config["link"])
                list_device = list()
                arr_device = config["devices"]
                for dev in arr_device:
                    device = devices()
                    device.set_platform_name(check_att_is_exist(dev, "platformName"))
                    device.set_is_headless((dev, "is_headless"))
                    device.set_wait(check_att_is_exist(dev, "wait"))
                    device.set_time_page_load(check_att_is_exist(dev, "time_page_load"))
                    device.set_auto_download_driver(check_att_is_exist(dev, "auto_download_driver"))
                    device.set_driver_from_path(check_att_is_exist(dev, "driver_version"))
                    device.set_app_package(check_att_is_exist(dev, "appPackage"))
                    device.set_app_activity(check_att_is_exist(dev, "appActivity"))
                    list_device.append(device)
                stage_env.set_list_devices(list_device)
                list_env.append(stage_env)
        env.set_list_env(list_env)
        return env

te = read_configuration()
env = te.read()
listss = env.get_list_env()
env_1 = listss[1 ]
arr_list = env_1.get_list_devices()
for arr in arr_list:
    print(arr.get_platform_name())
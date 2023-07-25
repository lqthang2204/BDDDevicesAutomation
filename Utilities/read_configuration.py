import yaml
import os
from yaml import SafeLoader
import json
from Configuration.configuration_env import environment_config
from Configuration.devices import devices
from Utilities.common import common_device
from Configuration.stage import stage
from Configuration.api_facets import api


class read_configuration:
    def read(self):
        config_file_path = os.path.dirname(os.path.dirname(__file__)) + "/environments.yml"
        with open(config_file_path) as configs_env:
            config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
            json_result = json.dumps(config_file)
            json_object = json.loads(json_result)
            # print(json_object)
            arr_config = json_object["env"]
            list_stage = []
            env = environment_config()
            list_device = list()
            # stage_env = [config for config in arr_config]
            # arr_device = stage_env[0]['devices']
            for config in arr_config:
                stage_env = stage()
                stage_env.set_stage_name(config["stage"])
                stage_env.set_list_link(config["link"])
                arr_device = config["devices"]
                arr_link_api = config["api-facets"]
                stage_env.set_api_facets(arr_link_api)
                list_device = [dev for dev in arr_device]
                stage_env.set_list_devices(list_device)
                list_stage.append(stage_env)
            env.set_list_stage(list_stage)
        return env
# te = read_configuration()
# env = te.read()
# listss = env.get_list_env()
# env_1 = listss[1 ]
# arr_list = env_1.get_list_devices()
# for arr in arr_list:
#     print(arr.get_platform_name())

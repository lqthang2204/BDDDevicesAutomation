import yaml
import os
from yaml import SafeLoader
import json

class read_configuration:
    def read(self):
        config_file_path = os.path.dirname(os.path.dirname(__file__)) + "/environments.yml"
        with open(config_file_path) as configs_env:
            config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
            json_result = json.dumps(config_file)
            json_object = json.loads(json_result)
            arr_config = json_object["env"]
            stage_env = [config for config in arr_config]
        return stage_env

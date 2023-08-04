import json
import os

import yaml
from yaml import SafeLoader



class read_configuration:
    def read(self, stage_name):
        config_file_path = os.path.dirname(os.path.dirname(__file__)) + "/environments.yml"
        with open(config_file_path) as configs_env:
            config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
            json_result = json.dumps(config_file)
            arr_stage = json.loads(json_result)['env']
            for stage_env in arr_stage:
                if stage_env['stage'] == stage_name:
                    return stage_env

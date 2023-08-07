import json
import os

import yaml
from yaml import SafeLoader



class read_configuration:

    project_folder = os.path.dirname(os.path.dirname(__file__))

    def read(self, stage_name):
        config_file_path = self.project_folder + "/environments.yml"
        with open(config_file_path) as configs_env:
            config_file = yaml.load(configs_env.read(), Loader=SafeLoader)
            json_result = json.dumps(config_file)
            arr_stage = json.loads(json_result)['env']
            for stage_env in arr_stage:
                if stage_env['stage'] == stage_name:
                    return stage_env

    def read_api_endpoints(self):
        api_endpoint_path = os.path.join(self.project_folder, "resources", "api", "endpoints" ,'api-endpoints.yml')
        with open(api_endpoint_path) as api_endpoints_file:
            api_endpoint = yaml.safe_load(api_endpoints_file.read())
        return api_endpoint


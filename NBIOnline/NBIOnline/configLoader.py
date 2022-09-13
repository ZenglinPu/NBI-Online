import os

import yaml


# 用于加载外部yaml配置，直接使用nbi_conf.configs['']
class ConfigLoader:
    def __init__(self):
        self.configs = None
        current_path = os.path.abspath(__file__)
        self.config_path = os.path.dirname(os.path.dirname(os.path.dirname(current_path))) + '/conf/nbi-config.yaml'
        with open(self.config_path, 'r') as f:
            # configs: 含有配置参数键值对的字典
            self.configs = yaml.load(f, Loader=yaml.FullLoader)

        assert None not in self.configs.values(), "Make sure every config setting in nbi-config.yaml is not none"


# Import nbi_config to get configs
nbi_conf = ConfigLoader()

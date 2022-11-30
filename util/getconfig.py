import yaml
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# 获取配置文件
class GetYamlConfig(object):
    def __init__(self, basedir=None, path=None):
        self.basedir = basedir if basedir else BASE_DIR
        self.path = f"{self.basedir}/{path}" if path else f"{self.basedir}/config/config.yaml"

    def get_config(self, service=None) -> dict:
        try:
            with open(self.path, 'r') as f:
                cfg = yaml.full_load(f)
                if service:
                    assert cfg[service], f"没有对应 {service} 配置，检查config.yaml 是否存在对应配置信息！！！"
                    config_data = cfg[service]
                    return config_data
                else:
                    return cfg
        except Exception as e:
            print("获取配置失败，请检查！！！", e)

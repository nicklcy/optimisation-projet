from pathlib import Path

from basket.env.env import Env
from basket.utils.yaml import read_yaml_file


def load_env_from_yaml(filename: Path):
    yaml_content = read_yaml_file(filename)
    env_config = yaml_content['environment']

    env_typ = env_config['type']
    del env_config['type']
    if env_typ == 'basic':
        return Env(**env_config)
    else:
        raise ValueError

from pathlib import Path

from basket.optimizer.BGDOptimizer import BGDOptimizer
from basket.optimizer.SGDOptimizer import SGDOptimizer
from basket.utils.yaml import read_yaml_file

def load_optimizer_from_yaml(filename: Path):
    yaml_content = read_yaml_file(filename)
    opt_config = yaml_content['optimizer']

    opt_type = opt_config['type']
    del opt_config['type']

    if opt_type == 'BGD':
        return BGDOptimizer(**opt_config)
    elif opt_type == 'SGD':
        return SGDOptimizer(**opt_config)
    else:
        raise NotImplementedError

from pathlib import Path

from basket.loss.distance_loss import DistanceLoss
from basket.utils.yaml import read_yaml_file


def load_loss_from_yaml(env, sim, filename: Path):
    yaml_content = read_yaml_file(filename)
    loss_config = yaml_content['loss']

    loss_typ = loss_config['type']
    del loss_config['type']

    if loss_typ == 'distance':
        return DistanceLoss(env, sim, **loss_config)
    else:
        raise ValueError

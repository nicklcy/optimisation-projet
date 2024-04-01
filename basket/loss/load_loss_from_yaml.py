from pathlib import Path

from basket.loss.basic_loss import BasicLoss
from basket.loss.board_loss import BoardLoss
from basket.utils.yaml import read_yaml_file


def load_loss_from_yaml(env, sim, filename: Path):
    yaml_content = read_yaml_file(filename)
    loss_config = yaml_content['loss']

    loss_typ = loss_config['type']
    del loss_config['type']

    if loss_typ == 'basic':
        return BasicLoss(env, sim, **loss_config)
    elif loss_typ == 'board':
        return BoardLoss(env, sim, **loss_config)
    else:
        raise ValueError

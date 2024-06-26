import os
import time
import argparse
from basket.env import load_env_from_yaml
from basket.sim import SymplecticEulerSimulator
from basket.ui import TaichiUI
from basket.utils.yaml import dump_exp_yaml


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'collide_env.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)

    return parser.parse_args()


def main(args):
    env = load_env_from_yaml(args.env)

    sim = SymplecticEulerSimulator(env)
    ui = TaichiUI(sim, res=50)

    # tap_times = [0.4, 0.8, 1.2, 1.5]
    tap_times = None
    ui.play(tap_times)

    dump_exp_yaml(os.path.join('configs', 'exp', 'test_board_collide.yaml'), {'env': args.env}, tap_times)


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

import os
import time
import argparse
from basket.env import load_env_from_yaml
from basket.sim import AnalyticalSimulator
from basket.loss import DistanceLoss
from basket.ui import TaichiUI


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'basic_env.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)

    return parser.parse_args()


def main(args):
    env = load_env_from_yaml(args.env)

    sim = AnalyticalSimulator(env)
    ui = TaichiUI(sim)

    ui.play()

    loss = DistanceLoss(env, sim)
    print(loss.get_loss(ui.sim.tap_times))


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

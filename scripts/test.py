import os
import time
import argparse
from basket.env import Env
from basket.sim import AnalyticalSimulator
from basket.ui import TaichiUI


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'basic_env.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)

    return parser.parse_args()


def main(args):
    env = Env.load_from_yaml(args.env)

    sim = AnalyticalSimulator(env)
    ui = TaichiUI(sim)

    start_tme = time.time()
    while sim.in_x_bounds():
        cur_tme = time.time() - start_tme
        if ui.has_tapped():
            sim.add_tap_time(cur_tme)
        sim.sim_to_time(cur_tme)
        ui.step()


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

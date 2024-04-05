import os
import time
import argparse
from basket.env import load_env_from_yaml
from basket.sim import SymplecticEulerSimulator
from basket.utils.yaml import dump_exp_yaml
from basket.vis import MatplotlibVis


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'collide_env.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)

    return parser.parse_args()


def main(args):
    env = load_env_from_yaml(args.env)

    sim = SymplecticEulerSimulator(env, dt=0.001)
    tap_times = [0.42441606521606445, 0.7, 0.8009703254699707, 1.1920]
    sim.tap_times = tap_times
    sim.sim_to_target()

    vis = MatplotlibVis(env)
    vis.add_trajectory(sim)
    vis.show()

    dump_exp_yaml(os.path.join('configs', 'exp', 'test_basket_collide.yaml'), {'env': args.env}, tap_times)


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

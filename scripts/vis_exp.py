import os
import time
import argparse
from basket.env import load_env_from_yaml
from basket.sim import AnalyticalSimulator, SymplecticEulerSimulator
from basket.utils.yaml import read_yaml_file
from basket.vis import MatplotlibVis


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    exp_path = os.path.join(folder_path, '..', 'exp')
    default_exp_dir = ''
    for dir in os.listdir(exp_path):
        tmp_path = os.path.join(exp_path, dir)
        if os.path.isdir(tmp_path):
            default_exp_dir = tmp_path
            break

    parser = argparse.ArgumentParser()
    parser.add_argument('--exp-dir', type=str, default=default_exp_dir)
    parser.add_argument('--dst', type=str, default='')

    return parser.parse_args()


def main(args):
    config_path = os.path.join(args.exp_dir, 'config.yaml')

    if not args.dst:
        args.dst = os.path.join(args.exp_dir, 'traj.png')

    env = load_env_from_yaml(config_path)

    vis = MatplotlibVis(env)

    config_content = read_yaml_file(config_path)
    tap_times = config_content['tap_times']
    sim_config = config_content['sim']

    sim_typ = sim_config['type']

    if sim_typ == 'analytical':
        sim = AnalyticalSimulator(env, tap_times=tap_times)
    elif sim_typ == 'euler':
        sim = SymplecticEulerSimulator(env, dt=sim_config['dt'], tap_times=tap_times)
    else:
        raise ValueError

    sim.sim_trajectory()

    vis.add_trajectory(sim)

    vis.show()
    vis.save_file(args.dst)


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

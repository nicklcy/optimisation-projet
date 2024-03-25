import os
import argparse
from basket.env import load_env_from_yaml
from basket.sim import AnalyticalSimulator
from basket.loss import load_loss_from_yaml
from basket.optimizer import load_optimizer_from_yaml
from basket.ui import TaichiUI


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env_configs', 'basic_env.yaml')
    default_loss_config = os.path.join(configs_path, 'loss', 'distance_loss.yaml')
    default_opt_config = os.path.join(configs_path, 'opt', 'BGD.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)
    parser.add_argument('--loss', type=str, default=default_loss_config)
    parser.add_argument('--opt', type=str, default=default_opt_config)

    return parser.parse_args()


def main(args):
    env = load_env_from_yaml(args.env)

    sim = AnalyticalSimulator(env)
    ui = TaichiUI(sim)

    ui.play()

    loss = load_loss_from_yaml(env, sim, args.loss)
    opt = load_optimizer_from_yaml(args.opt)
    tap_times = ui.sim.tap_times

    for i in range(200):
        if (i + 1) % 100 == 0:
            ui.play(tap_times)
        loss_with_grad = loss.get_loss(tap_times)
        print(i, loss_with_grad, tap_times)
        opt.optim(tap_times, loss_with_grad)


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

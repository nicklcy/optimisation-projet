import os
import time
import argparse
import random
from basket.env import load_env_from_yaml
from basket.loss import load_loss_from_yaml
from basket.optimizer import load_optimizer_from_yaml
from basket.sim.euler_sim import SymplecticEulerSimulator
from basket.ui import TaichiUI
from basket.utils.yaml import read_yaml_file, dump_exp_yaml


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'air_friction_env.yaml')
    default_loss_config = os.path.join(configs_path, 'loss', 'board_loss.yaml')
    default_opt_config = os.path.join(configs_path, 'opt', 'BGD.yaml')
    default_exp_folder = os.path.join(folder_path, '..', 'exp')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)
    parser.add_argument('--loss', type=str, default=default_loss_config)
    parser.add_argument('--opt', type=str, default=default_opt_config)
    parser.add_argument('--N', type=int, default=4)
    parser.add_argument('--exp-dir', type=str, default=default_exp_folder)
    parser.add_argument('--init-tap-times-yaml', type=str, default='')

    return parser.parse_args()


def initialize_tap_times(env, N):
    dx = env.target_pos[0] - env.init_pos[0]
    vel_x = env.init_vel[0]
    tme = dx.val / vel_x.val

    tme_lb, tme_ub = env.min_tap_interval, tme * .8
    init_list = []
    for i in range(N):
        init_list.append(tme_lb + random.random() * (tme_ub - tme_lb))
    for i in range(N):
        for j in range(i):
            if init_list[i] < init_list[j]:
                init_list[i], init_list[j] = init_list[j], init_list[i]

    return init_list


def main(args):
    env = load_env_from_yaml(args.env)

    sim = SymplecticEulerSimulator(env)
    ui = TaichiUI(sim, res=50)

    loss = load_loss_from_yaml(env, sim, args.loss)
    opt = load_optimizer_from_yaml(args.opt)

    tap_times = ui.sim.tap_times
    if args.init_tap_times_yaml:
        content = read_yaml_file(args.init_tap_times_yaml)
        if 'init_tap_times' in content.keys():
            tap_times = content['init_tap_times']
    if not tap_times:
        tap_times = initialize_tap_times(env, args.N)
    init_tap_times = [x for x in tap_times]

    min_loss, min_tap_times = None, []

    csv_table = []

    for i in range(500):
        if (i + 0) % 10 == 0:
            ui.play(tap_times)
        loss_with_grad = loss.get_loss(tap_times)

        if min_loss is None or loss_with_grad.val < min_loss:
            min_loss = loss_with_grad.val
            min_tap_times = [x for x in tap_times]

        csv_table.append([loss_with_grad.val] + tap_times)

        print(i, loss_with_grad, tap_times)

        if loss_with_grad.val < 0.5:
            break
        opt.optim(tap_times, loss_with_grad)

    print('Min_loss:', min_loss)
    print('Tap_times:', min_tap_times)
    ui.play(min_tap_times)

    exp_dir = os.path.join(args.exp_dir, str(int(time.time())))
    os.mkdir(exp_dir)

    exp_config_dict = {
        'env': args.env,
        'loss': args.loss,
        'opt': args.opt,
        'sim': {
            'type': 'euler',
            'dt': sim.dt
        }
    }
    env_config_path = os.path.join(exp_dir, 'config.yaml')
    dump_exp_yaml(env_config_path, exp_config_dict, min_tap_times, init_tap_times)

    csv_line_str = [','.join(map(str, csv_row)) for csv_row in csv_table]
    csv_content = '\n'.join(csv_line_str)
    csv_path = os.path.join(exp_dir, 'loss.csv')
    with open(csv_path, 'w') as f:
        f.write(csv_content)


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

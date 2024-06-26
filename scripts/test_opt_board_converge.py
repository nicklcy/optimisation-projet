import os
import argparse
from basket.env import load_env_from_yaml
from basket.sim import SymplecticEulerSimulator
from basket.loss import load_loss_from_yaml
from basket.optimizer import load_optimizer_from_yaml
from basket.ui import TaichiUI
from basket.vis import MatplotlibVis


def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'collide_env.yaml')
    default_loss_config = os.path.join(configs_path, 'loss', 'board_loss.yaml')
    default_opt_config = os.path.join(configs_path, 'opt', 'BGD.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)
    parser.add_argument('--loss', type=str, default=default_loss_config)
    parser.add_argument('--opt', type=str, default=default_opt_config)

    return parser.parse_args()


def main(args):
    env = load_env_from_yaml(args.env)

    sim = SymplecticEulerSimulator(env, dt=0.002)
    ui = TaichiUI(sim, res=50)

    # ui.play()

    loss = load_loss_from_yaml(env, sim, args.loss)
    opt = load_optimizer_from_yaml(args.opt)
    tap_times = ui.sim.tap_times
    tap_times = [0.40452335825276353, 0.7230319153573838, 0.9785392521310986, 1.4099850733984653]

    vis = MatplotlibVis(env)

    min_loss, min_tap_times = None, []

    for i in range(500):
        if (i + 0) % 1 == 0 and False:
            print('Playing tap_times:', tap_times)
            ui.play(tap_times)
        loss_with_grad = loss.get_loss(tap_times)

        vis.add_trajectory(sim)

        if min_loss is None or loss_with_grad.val < min_loss:
            min_loss = loss_with_grad.val
            min_tap_times = [x for x in tap_times]

        print(i, loss_with_grad, tap_times)

        if loss_with_grad.val < 1e-3: break

        opt.optim(tap_times, loss_with_grad)

    print('Min_loss:', min_loss)
    print('Tap_times:', min_tap_times)
    ui.play(min_tap_times)

    vis.show()


if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)

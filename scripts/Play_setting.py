import taichi as ti
import os
import argparse
from basket.env import load_env_from_yaml
from basket.sim import SymplecticEulerSimulator
from basket.loss import load_loss_from_yaml
from basket.optimizer import load_optimizer_from_yaml
from basket.ui import TaichiUI
from basket.ui.ui import UI
import numpy as np
from basket.utils.yaml import setting_write_in as dump
from pathlib import Path

def parse_args():
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'air_friction_env.yaml')
    default_loss_config = os.path.join(configs_path, 'loss', 'board_loss.yaml')
    default_opt_config = os.path.join(configs_path, 'opt', 'BGD.yaml')

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', type=str, default=default_env_config)
    parser.add_argument('--loss', type=str, default=default_loss_config)
    parser.add_argument('--opt', type=str, default=default_opt_config)

    return parser.parse_args()


class SUI(TaichiUI):
    def __init__(self, sim, tap_times=None, use_gui=True, 
                 res=100, background_color=16777215, ball_color=0):
        super().__init__(sim, tap_times, use_gui, res, background_color, ball_color)
        self.res = res
        self.ball_r =  self.gui.slider('Ball', 0.1, 3, step=1)
        self.ball_r.value = 1
        self.ring_r =  self.gui.slider('Ring', 0.1, 3, step=1)
        self.ring_r.value = 1
        self.basket_r =  self.gui.slider('Basket', 0.1, 3, step=1)
        self.basket_r.value = 1
        self.ballx = self.gui.label('Ball_pos_x:A and D')
        self.ballx.value = 0
        self.bally = self.gui.label('Ball_pos_y:W and S')
        self.bally.value = 0
        self.targetx = self.gui.label('Target_pos_x:LEFT and RIGHT')
        self.targetx.value = 0
        self.targety = self.gui.label('Target_pos_y:UP and DOWN')
        self.targety.value = 0
        self.coeff_bounce = self.gui.slider('Bounce', 0, 1, step=1)
        self.coeff_bounce.value = 0.6
        self.air = self.gui.slider('Air_fric', 0, 0.05, step=1)
        self.air.value = 0.01
        self.Human = self.gui.button("Human")
        self.AI = self.gui.button("AI")
        self.Mode = False
    def render(self):
        env = self.sim.env
        self.ball_radius = (env.ball_radius * self.res * self.ball_r.value).val
        self.basket_ring_radius = (env.basket_ring_radius * self.res * self.ring_r.value).val
        for e in self.gui.get_events(self.gui.PRESS):
            if e.key == self.gui.ESCAPE:
                self.use_gui = False
            elif e.key == 'a':
                self.ballx.value -= 0.01
            elif e.key == 'd':
                self.ballx.value += 0.01
            elif e.key == 's':
                self.bally.value -= 0.01
            elif e.key == 'w':
                self.bally.value += 0.01
            elif e.key == ti.GUI.LEFT:
                self.targetx.value -= 0.01
            elif e.key == ti.GUI.RIGHT:
                self.targetx.value += 0.01
            elif e.key == ti.GUI.DOWN:
                self.targety.value -= 0.01
            elif e.key == ti.GUI.UP:
                self.targety.value += 0.01
            elif e.key == 'r':
                self.ballx.value = abs(np.random.normal(0, 0.1))
                self.bally.value = np.random.normal(0, 0.1)
                self.targety.value = np.random.normal(0, 0.1)
                self.targetx.value = np.random.normal(0, 0.1)
            elif e.key == self.Human:
                self.use_gui = False
            elif e.key == self.AI:
                self.Mode = True
                self.use_gui = False

                

        # dessiner la boule
        self.gui.circles(np.array([self.get_pos(env.init_pos)] + np.array([self.ballx.value,self.bally.value])),
                         radius=self.ball_radius, color=self.ball_color)

        # dessiner le but
        self.gui.circles(np.array([self.get_pos(env.target_pos)]) + np.array([self.targetx.value, self.targety.value]),
                         radius=self.ball_radius, color=0xFF0000)

        # dessiner le basket
        basket_1 = [env.target_pos[0] - env.basket_radius*self.basket_r.value, env.target_pos[1]]
        basket_2 = [env.target_pos[0] + env.basket_radius*self.basket_r.value, env.target_pos[1]]
        self.gui.circles(np.array([self.get_pos(basket_1), self.get_pos(basket_2)] + np.array([self.targetx.value, self.targety.value])),
                         radius=self.basket_ring_radius, color=0xFF00FF)

        # dessiner le panneau
        if env.board_width:
            board_x1 = basket_2[0] + env.basket_ring_radius * .5 * self.ring_r.value
            board_x2 = board_x1 + env.board_width
            board_y1 = basket_2[-1]
            board_y2 = board_y1 + env.board_height
            self.gui.triangles(np.array([self.get_pos((board_x1, board_y1))] * 2) + np.array([self.targetx.value, self.targety.value]),
                               np.array([self.get_pos((board_x1, board_y2)),
                                         self.get_pos((board_x2, board_y1))])+ np.array([self.targetx.value, self.targety.value]),
                               np.array([self.get_pos((board_x2, board_y2))] * 2)+ np.array([self.targetx.value, self.targety.value]),
                               color=0xFF00FF)

def main(args):
    env = load_env_from_yaml(args.env)
    sim = SymplecticEulerSimulator(env, dt=0.01)
    ui = SUI(sim, res=50)
    ui.InitPos()
    folder_path = os.path.abspath(os.path.dirname(__file__))
    configs_path = os.path.join(folder_path, '..', 'configs')
    default_env_config = os.path.join(configs_path, 'env', 'air_friction_env.yaml')
    dump(Path(default_env_config), 'ball_radius', ui.ball_radius/ui.res)
    dump(Path(default_env_config), 'basket_ring_radius', ui.basket_ring_radius/ui.res)
    dump(Path(default_env_config), 'basket_radius', (env.basket_radius * ui.basket_r.value).val)
    bounds = sim.env.bounds
    dump(Path(default_env_config), 'init_pos',[ui.ballx.value * (bounds[0][1] - bounds[0][0]).val, ui.bally.value * (bounds[1][1] - bounds[1][0]).val] )
    dump(Path(default_env_config), 'target_pos',[ui.targetx.value * (bounds[0][1] - bounds[0][0]).val, ui.targety.value * (bounds[1][1] - bounds[1][0]).val] )
    dump(Path(default_env_config), 'coeff_bounce', ui.coeff_bounce.value)
    dump(Path(default_env_config), 'air_friction', ui.air.value)
    return ui.Mode

def PlaySetting():
    args = parse_args()
    print('Arguments:', args)
    mode = main(args)
    print(mode)
    return mode

if __name__ == '__main__':
    args = parse_args()
    print('Arguments:', args)
    main(args)


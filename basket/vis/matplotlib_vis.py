from basket.vis.vis import Vis
from basket.utils.maths import get_val
import numpy as np
import matplotlib.pyplot as plt

class MatplotlibVis(Vis):
    def __init__(self,
                 env=None,
                 bounds=None,
                 ball_radius=None,
                 basket_radius=None,
                 basket_ring_radius=None,
                 board_width=None,
                 board_height=None,
                 scale=0.5,
                 dpi=256,
                 traj_color=(0, 0, 1),
                 target_color=(1, 0, 0),
                 ring_color=(0, 0, 0),
                 board_color=(0, 0, 0)):
        super().__init__(env, bounds, ball_radius,
                         basket_radius, basket_ring_radius,
                         board_width, board_height)

        self.traj_color = traj_color
        self.target_color = target_color
        self.ring_color = ring_color
        self.board_color = board_color

        siz_x = (self.bounds[0][1] - self.bounds[0][0]).val * scale
        siz_y = (self.bounds[1][1] - self.bounds[1][0]).val * scale

        self.fig, self.ax = plt.subplots(1, 1,
                                         figsize=(siz_x, siz_y))
        ax = self.ax
        ax.spines['left'].set_position(('data', 0))
        ax.spines['bottom'].set_position(('data', 0))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.set_xlim(*get_val(self.bounds[0]))
        ax.set_ylim(*get_val(self.bounds[1]))


    def add_trajectory(self, sim, env=None, traj_color=0x00FF00):
        if env is None:
            env = self.default_env

        target = env.target_pos
        basket_1_pos = get_val([target[0] - self.basket_radius, target[1]])
        basket_2_pos = get_val([target[0] + self.basket_radius, target[1]])
        basket_1 = plt.Circle(basket_1_pos, self.basket_ring_radius.val, fc=self.ring_color)
        basket_2 = plt.Circle(basket_2_pos, self.basket_ring_radius.val, fc=self.ring_color)
        self.ax.add_patch(basket_1)
        self.ax.add_patch(basket_2)

        board_pos = basket_2_pos
        board_pos[0] += self.basket_ring_radius.val * .5
        board = plt.Rectangle(board_pos, self.board_width.val, self.board_height.val, fc=self.board_color)
        self.ax.add_patch(board)

        traj_pos = np.array(get_val(sim.pos_list))
        self.ax.plot(traj_pos[:, 0], traj_pos[:, 1], c=self.traj_color)

        for tap_time in sim.tap_times:
            for i in range(len(sim.tme_list) - 1):
                if sim.tme_list[i] <= tap_time < sim.tme_list[i+1]:
                    self.ax.scatter([traj_pos[i, 0]], [traj_pos[i, 1]], c=self.traj_color)

        print('sim.collide_list:', sim.collide_list)
        for id in sim.collide_list:
            if id - 1 in sim.collide_list:
                continue
            ball = plt.Circle((traj_pos[id, 0], traj_pos[id, 1]),
                              self.ball_radius.val, fc=self.traj_color + (0.5,))
            self.ax.add_patch(ball)

    def show(self):
        plt.show()

    def save_file(self, filename):
        self.fig.savefig(filename)

import taichi as ti
import numpy as np
from basket.ui.ui import UI


class LegacyTaichiUI(UI):
    def __init__(self, sim, tap_times=None, use_gui=True,
                 res=100, background_color=0xFFFFFF,
                 ball_color=0x0000FF):
        super().__init__(sim, tap_times, use_gui)

        env = self.sim.env
        bounds = env.bounds
        self.ball_radius = (env.ball_radius * res).val
        self.basket_ring_radius = (env.basket_ring_radius * res).val

        self.ball_color = ball_color
        ui_res = (res * (bounds[0][1] - bounds[0][0]).val,
                  res * (bounds[1][1] - bounds[1][0]).val)
        self.board_width = (env.board_width * res).val * .5

        self.gui = ti.GUI("Basket", res=ui_res, background_color=background_color)

    def has_tapped(self):
        if self.interact and self.gui.get_event(ti.GUI.PRESS):
            return self.gui.is_pressed(ti.GUI.SPACE)

    def get_pos(self, pos):
        bounds = self.sim.env.bounds
        screen_x = (pos[0] - bounds[0][0]) / (bounds[0][1] - bounds[0][0])
        screen_y = (pos[1] - bounds[1][0]) / (bounds[1][1] - bounds[1][0])
        return np.array([screen_x.val, screen_y.val])

    def render(self):
        env = self.sim.env
        # dessiner le but
        self.gui.circles(np.array([self.get_pos(env.target_pos)]),
                         radius=self.ball_radius, color=0xFF0000)

        # dessiner la boule
        self.gui.circles(np.array([self.get_pos(self.sim.cur_pos)]),
                         radius=self.ball_radius, color=self.ball_color)

        # dessiner le basket
        basket_1 = [env.target_pos[0] - env.basket_radius, env.target_pos[1]]
        basket_2 = [env.target_pos[0] + env.basket_radius, env.target_pos[1]]
        self.gui.circles(np.array([self.get_pos(basket_1), self.get_pos(basket_2)]),
                         radius=self.basket_ring_radius, color=0x000000)

        # dessiner le panneau
        if env.board_width:
            board_x1 = basket_2[0] + env.basket_ring_radius * .5
            board_x2 = board_x1 + env.board_width
            board_y1 = basket_2[-1]
            board_y2 = board_y1 + env.board_height
            self.gui.triangles(np.array([self.get_pos((board_x1, board_y1))] * 2),
                               np.array([self.get_pos((board_x1, board_y2)),
                                         self.get_pos((board_x2, board_y1))]),
                               np.array([self.get_pos((board_x2, board_y2))] * 2),
                               color=0x000000)

    def step(self):
        self.render()
        if self.use_gui:
            self.gui.show()

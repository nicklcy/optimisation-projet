import taichi as ti
import numpy as np
from basket.ui.ui import UI


class TaichiUI(UI):
    def __init__(self, sim, tap_times=None, use_gui=True,
                 res=1024, background_color=0xFFFFFF,
                 ball_radius=20, ball_color=0x000000):
        super().__init__(sim, tap_times, use_gui)

        self.ball_radius, self.ball_color = ball_radius, ball_color

        self.gui = ti.GUI("Basket", res=res, background_color=background_color)

    def has_tapped(self):
        if self.interact and self.gui.get_event(ti.GUI.PRESS):
            return self.gui.is_pressed(ti.GUI.SPACE)

    def render(self):
        bounds = self.sim.env.bounds
        pos_x = (self.sim.cur_pos[0] - bounds[0][0]) / (bounds[0][1] - bounds[0][0])
        pos_y = (self.sim.cur_pos[1] - bounds[1][0]) / (bounds[1][1] - bounds[1][0])

        self.gui.circles(np.array([[pos_x.val, pos_y.val]]),
                         radius=self.ball_radius, color=self.ball_color)

        target = self.sim.env.target_pos
        pos_x = (target[0] - bounds[0][0]) / (bounds[0][1] - bounds[0][0])
        pos_y = (target[1] - bounds[1][0]) / (bounds[1][1] - bounds[1][0])

        self.gui.circles(np.array([[pos_x.val, pos_y.val]]),
                         radius=self.ball_radius, color=0xFF0000)
    def step(self):
        self.render()
        if self.use_gui:
            self.gui.show()

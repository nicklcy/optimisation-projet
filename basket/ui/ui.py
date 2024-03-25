import time


class UI:
    def __init__(self, sim, tap_times=None, use_gui=True):
        self.sim = sim
        self.interact = tap_times is None
        self.tap_times = tap_times
        self.use_gui = use_gui
        if self.interact:
            assert self.use_gui

    def has_tapped(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def play(self, tap_times=None):
        interactive = tap_times is None
        self.sim.reset(tap_times=tap_times)

        start_tme = time.time()
        while self.sim.in_x_bounds():
            cur_tme = time.time() - start_tme
            if interactive and self.has_tapped():
                self.sim.add_tap_time(cur_tme)
            self.sim.sim_to_time(cur_tme)
            self.step()

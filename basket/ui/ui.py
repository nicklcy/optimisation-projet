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


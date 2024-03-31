from basket.scalar import Scalar


class Simulator:
    def __init__(self, env, init_tme: float = 0, tap_times=None):
        self.env = env
        self.reset(init_tme, tap_times)

    def reset(self, init_tme: float = 0, tap_times=None):
        self.init_tme = init_tme
        self.cur_tme = Scalar(init_tme)
        self.cur_pos = list(Scalar.to_scalar_iterable(self.env.init_pos))
        self.cur_vel = list(Scalar.to_scalar_iterable(self.env.init_vel))
        self.actual_tap_times = 0

        self.pos_list = []
        self.vel_list = []

        self.last_tap = None

        if tap_times is not None:
            self.tap_times = tap_times
            self.interactive = False
        else:
            self.tap_times = []
            self.interactive = True

    def add_tap_time(self, tme: float):
        assert tme >= self.cur_tme, "Le temps ajouté est trop tard"
        self.tap_times.append(tme)

    def sim_to_time(self, tme: float):
        raise NotImplementedError

    def sim_to_target(self):
        raise NotImplementedError

    def in_x_bounds(self):
        return self.env.bounds[0][0] <= self.cur_pos[0] and \
            self.cur_pos[0].val <= self.env.bounds[0][1]

    def in_y_bounds(self):
        return self.env.bounds[1][0] <= self.cur_pos[1] and \
            self.cur_pos[1] <= self.env.bounds[1][1]

    def in_bounds(self):
        return self.in_x_bounds() and self.in_y_bounds()

    def can_continue(self):
        if not self.in_x_bounds():
            return False
        if self.cur_pos[1] < self.env.bounds[1][0]:
            if not self.interactive and self.cur_tme.val > self.tap_times[-1]:
                return False
        return True

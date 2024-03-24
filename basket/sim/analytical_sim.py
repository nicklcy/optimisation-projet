from basket.scalar import Scalar
from basket.sim.sim import Simulator


class AnalyticalSimulator(Simulator):
    def __init__(self, env, init_tme=0, tap_times=None):
        super().__init__(env, init_tme, tap_times)

    def _to_time_no_tap(self, tme):
        assert tme.val >= self.cur_tme.val

        elapsed = tme - self.cur_tme
        accel = self.env.gravity

        end_vel_x = self.cur_vel[0] + elapsed * accel[0]
        end_vel_y = self.cur_vel[1] + elapsed * accel[1]

        self.cur_pos[0] += (self.cur_vel[0] + end_vel_x) * elapsed * .5
        self.cur_pos[1] += (self.cur_vel[1] + end_vel_y) * elapsed * .5
        self.cur_vel = [end_vel_x, end_vel_y]
        print('cur_pos:', self.cur_pos)

        self.cur_tme = tme.clone()

    def sim_to_time(self, tme):
        assert tme >= self.cur_tme.val

        min_tap = self.cur_tme.val
        if self.last_tap is not None:
            tap_bound = self.last_tap + self.env.min_tap_interval
            if tap_bound > min_tap:
                min_tap = tap_bound

        for id, tap_time in enumerate(self.tap_times):
            if tap_time < min_tap:
                continue
            if tap_time > tme:
                break
            self._to_time_no_tap(Scalar.create_grad_1(tap_time, id))

            self.cur_vel[1] = self.env.tap_vel.clone()

            self.last_tap = tap_time
            tap_bound = self.last_tap + self.env.min_tap_interval

        self._to_time_no_tap(Scalar(tme))

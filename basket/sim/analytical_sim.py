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

        if self.cur_pos[0].val > self.env.target_pos[0].val - 1E-5:
            self.reach_target_x = True
        if self.cur_pos[0].val < self.env.target_pos[0].val + 1E-5:
            self.max_tap_time = tme.val

        self.pos_list.append((self.cur_pos[0].clone(), self.cur_pos[1].clone()))
        self.vel_list.append((self.cur_vel[0].clone(), self.cur_vel[1].clone()))
        self.tme_list.append(self.cur_tme.val)

        self.cur_tme = tme.clone()

    def sim_to_time(self, tme: float):
        assert tme >= self.cur_tme.val


        while True:
            while self.tap_id < len(self.tap_times):
                if self.tap_times[self.tap_id] < self.last_tap + self.env.min_tap_interval:
                    self.tap_id += 1
                else:
                    break
            if self.tap_id >= len(self.tap_times):
                break
            tap_time = self.tap_times[self.tap_id]
            if tap_time <= tme:
                self._to_time_no_tap(Scalar.create_grad_1(tap_time, self.tap_id))
                self.cur_vel[1] = Scalar(self.env.tap_vel)
                self.last_tap = tap_time
            else:
                break

        self._to_time_no_tap(Scalar(tme))

    def sim_to_target(self):
        dis1 = self.env.target_pos[0] - self.env.basket_radius - self.env.init_pos[0]
        elapsed_tme1 = dis1 / self.env.init_vel[0]
        tme1 = elapsed_tme1 + self.init_tme
        self.sim_to_time(tme1)

        elapsed_tme2 = self.env.basket_radius / self.env.init_vel[0]
        tme2 = tme1 + elapsed_tme2
        self.sim_to_time(tme2)

    def sim_trajectory(self, dt=0.01):
        tme = 0
        while self.can_continue():
            tme += dt
            self.sim_to_time(tme)

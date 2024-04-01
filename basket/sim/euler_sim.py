import math
import random
from basket.scalar import Scalar
from basket.sim.sim import Simulator
from basket.utils.maths import calc_sq_sum, calc_sqrt, arctan2, cos, sin


class SymplecticEulerSimulator(Simulator):
    def __init__(self, env, dt=0.001, init_tme=0, tap_times=None):
        super().__init__(env, init_tme, tap_times)

        self.dt = dt
        self.last_collide = False

        self.ball_radius = self.env.ball_radius
        self.circles = []
        for k in [-1, 1]:
            center_x = env.target_pos[0] + env.basket_radius * k
            center_y = env.target_pos[1]
            self.circles.append(((center_x, center_y), env.basket_ring_radius))
        self.board_x = env.target_pos[0] + \
            env.basket_radius + env.basket_ring_radius * .5
        self.board_y = [env.target_pos[1],
                        env.target_pos[1] + env.board_height]
        board_circ_x = self.board_x + env.board_width * .5
        board_circ_y = env.target_pos[1] + env.board_height
        self.circles.append(((board_circ_x, board_circ_y), env.board_width * .5))

        self.collide_board_id = []

    def collide_plane(self, theta):
        # Toucher avec une surface dont l'angle est theta
        cur_ang = arctan2(self.cur_vel[1], self.cur_vel[0])
        new_ang = theta * 2 - cur_ang
        cur_vel_mod = calc_sqrt(calc_sq_sum(self.cur_vel))
        new_vel_mod = cur_vel_mod * self.env.coeff_bounce
        self.cur_vel = [new_vel_mod * cos(new_ang), new_vel_mod * sin(new_ang)]

    def do_euler_integration(self, dt):
        accel = self.env.gravity
        vel_mod = calc_sqrt(calc_sq_sum(self.cur_vel))
        accel[0] -= self.env.air_friction * vel_mod * self.cur_vel[0]
        accel[1] -= self.env.air_friction * vel_mod * self.cur_vel[1]

        self.cur_vel[0] += accel[0] * dt
        self.cur_vel[1] += accel[1] * dt

        self.cur_tme += dt
        self.cur_pos[0] += self.cur_vel[0] * dt
        self.cur_pos[1] += self.cur_vel[1] * dt

        self.pos_list.append(
            (self.cur_pos[0].clone(), self.cur_pos[1].clone()))
        self.vel_list.append(
            (self.cur_vel[0].clone(), self.cur_vel[1].clone()))

    def step(self):
        # S'il touche avec les autres objets
        collide = False

        for circle in self.circles:
            (center_x, center_y), radius = circle
            radius += self.ball_radius
            delta = [self.cur_pos[0] - center_x, self.cur_pos[1] - center_y]
            dis = calc_sq_sum(delta)
            if dis.val < radius * radius:
                collide = True
                if not self.last_collide:
                    theta = arctan2(delta[1], delta[0]) + math.pi / 2
                    self.collide_plane(theta)

        if self.env.board_width:
            if self.board_y[0] < self.cur_pos[1] < self.board_y[1]:
                if self.board_x - self.env.ball_radius < self.cur_pos[0] < self.board_x:
                    # Collision avec le panneau
                    collide = True
                    if not self.last_collide:
                        self.collide_plane(Scalar(math.pi / 2))
                        self.collide_board_id.append(len(self.pos_list))

        self.last_collide = collide

        self.do_euler_integration(self.dt)

    def _to_time_no_tap(self, tme: float):
        while self.cur_tme.val + self.dt <= tme:
            self.step()

    def do_tap(self, tap_time: Scalar):
        assert tap_time >= self.cur_tme
        before_time = tap_time - self.cur_tme
        after_time = self.cur_tme + self.dt - tap_time

        self.do_euler_integration(before_time)
        self.cur_vel[1] = Scalar(self.env.tap_vel)
        self.do_euler_integration(after_time)

        self.last_tap = tap_time

    def sim_to_time(self, tme: float):
        assert tme >= self.cur_tme.val

        while self.cur_tme.val < tme:
            while self.tap_id < len(self.tap_times):
                if self.tap_times[self.tap_id] < self.last_tap + self.env.min_tap_interval:
                    self.tap_id += 1
                else:
                    break
            if self.tap_id >= len(self.tap_times):
                break
            tap_time = self.tap_times[self.tap_id]
            if tap_time <= tme:
                self._to_time_no_tap(tap_time)
                self.do_tap(Scalar.create_grad_1(tap_time, self.tap_id))
            else:
                break

        self._to_time_no_tap(tme)

    def sim_to_target(self):
        while self.can_continue():
            while self.tap_id < len(self.tap_times):
                if self.tap_times[self.tap_id] < self.last_tap + self.env.min_tap_interval:
                    self.tap_id += 1
                else:
                    break
            if self.tap_id < len(self.tap_times):
                if self.tap_times[self.tap_id] < self.cur_tme.val + self.dt:
                    self.do_tap(Scalar.create_grad_1(self.tap_times[self.tap_id], self.tap_id))
            self.step()

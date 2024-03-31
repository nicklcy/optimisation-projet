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
        self.board_x = env.target_pos[0] + env.basket_radius + env.basket_ring_radius * .5
        self.board_y = [env.target_pos[1], env.target_pos[1] + env.board_height]
        board_circ_x = self.board_x + env.board_width * .5
        board_circ_y = env.target_pos[1] + env.board_height
        self.circles.append(((board_circ_x, board_circ_y), env.board_width * .5))

    def collide_plane(self, theta):
        # Toucher avec une surface dont l'angle est theta
        cur_ang = arctan2(self.cur_vel[1], self.cur_vel[0])
        new_ang = theta * 2 - cur_ang
        cur_vel_mod = calc_sqrt(calc_sq_sum(self.cur_vel))
        new_vel_mod = cur_vel_mod * self.env.coeff_bounce
        self.cur_vel = [new_vel_mod * cos(new_ang), new_vel_mod * sin(new_ang)]

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
                if self.board_x - self.ball_radius < self.cur_pos[0] < self.board_x:
                    # Collision avec le panneau
                    collide = True
                    if not self.last_collide:
                        self.collide_plane(Scalar(math.pi / 2))

        self.last_collide = collide

        accel = self.env.gravity
        vel_mod = calc_sqrt(calc_sq_sum(self.cur_vel))
        accel[0] -= self.env.air_friction * vel_mod * self.cur_vel[0]
        accel[1] -= self.env.air_friction * vel_mod * self.cur_vel[1]

        self.cur_vel[0] += accel[0] * self.dt
        self.cur_vel[1] += accel[1] * self.dt

        self.cur_tme += self.dt
        self.cur_pos[0] += self.cur_vel[0] * self.dt
        self.cur_pos[1] += self.cur_vel[1] * self.dt

        self.pos_list.append((self.cur_pos[0].clone(), self.cur_pos[1].clone()))
        self.vel_list.append((self.cur_vel[0].clone(), self.cur_vel[1].clone()))

    def sim_to_time(self, tme: float):
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
            while self.cur_tme.val + self.dt < tap_time:
                self.step()

            delta_vel = Scalar.create_grad_1(val=1, id=id) * \
                (self.env.tap_vel - self.cur_vel[1].val)
            self.cur_vel[1] += delta_vel

            self.actual_tap_times += 1
            self.last_tap = tap_time
            tap_bound = self.last_tap + self.env.min_tap_interval

        while self.cur_tme.val < tme:
            self.step()

    def sim_to_target(self):
        dis1 = self.env.target_pos[0] - \
            self.env.basket_radius - self.env.init_pos[0]
        elapsed_tme1 = dis1 / self.env.init_vel[0]
        tme1 = elapsed_tme1 + self.init_tme
        self.sim_to_time(tme1)

        elapsed_tme2 = self.env.basket_radius / self.env.init_vel[0]
        tme2 = tme1 + elapsed_tme2
        self.sim_to_time(tme2)

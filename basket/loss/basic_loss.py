from basket.loss.loss import Loss
from basket.utils.maths import *


class BasicLoss(Loss):
    def __init__(self, env, sim,
                 dis_typ: str,
                 coeff_interval: float,
                 coeff_late: float,
                 coeff_ground: float,
                 coeff_dir: float):
        super().__init__(env, sim)

        assert dis_typ in ['L1', 'L2']
        self.dis_typ = dis_typ
        self.coeff_interval = coeff_interval
        self.coeff_late = coeff_late
        self.coeff_ground = coeff_ground
        self.coeff_dir = coeff_dir

        self.loss_funcs = [self.get_loss_1,
                           self.get_loss_2,
                           self.get_loss_3,
                           self.get_loss_4]

    def get_loss_1(self):
        pos = self.sim.pos_list[-1]

        target = self.env.target_pos

        if self.dis_typ == 'L1':
            return calc_abs(pos[1] - target[1])
        else:
            return calc_sq(pos[1] - target[1])

    def get_loss_2(self):
        loss = Scalar(0)
        tap_times = self.sim.tap_times
        mx_tap_time = self.sim.cur_tme - self.env.min_tap_interval
        for i in range(len(tap_times)):
            if i + 1 < len(tap_times):
                dt = Scalar.create_grad_1(tap_times[i + 1], i + 1) -  \
                    Scalar.create_grad_1(tap_times[i], i)
                diff = Scalar(self.env.min_tap_interval) - dt
                if diff.val > 0:
                    loss += diff * self.coeff_interval
            if i >= self.sim.actual_tap_times or tap_times[i] > mx_tap_time:
                diff = Scalar.create_grad_1(tap_times[i], i) - mx_tap_time
                loss += diff * self.coeff_late
        return loss

    def get_loss_3(self):
        # Obtenir la perte pour basket.y < self.env.ground_threshold
        loss = Scalar(0)
        for pos in self.sim.pos_list:
            height = pos[1] - self.env.ground_threshold
            if height.val < 0:
                if self.dis_typ == 'L1':
                    loss -= height
                else:
                    loss += calc_sq(height)
        loss *= self.coeff_ground
        return loss

    def get_loss_4(self):
        pos = self.sim.pos_list[-2]
        diff = self.env.target_pos[1] + \
            self.env.basket_ring_radius + self.env.ball_radius - pos[1]
        if diff.val > 0:
            return diff * self.coeff_dir
        else:
            return 0

    def get_loss(self, tap_times: list[float]):
        self.sim.reset(tap_times=tap_times)
        self.sim.sim_to_target()

        return sum([Scalar(loss_func()) for loss_func in self.loss_funcs],
                   start=Scalar(0))

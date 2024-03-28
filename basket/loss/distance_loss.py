from basket.loss.loss import Loss
from basket.utils.maths import *

class DistanceLoss(Loss):
    def __init__(self, env, sim, dis_typ: str = 'L1', coeff_dir: float = 10):
        super().__init__(env, sim)

        assert dis_typ in ['L1', 'L2']
        self.dis_typ = dis_typ
        self.coeff_dir = coeff_dir

    def get_loss(self, tap_times: list[float]):
        self.sim.reset(tap_times=tap_times)
        self.sim.sim_to_target()

        pos = self.sim.pos_list[-1]
        vel = self.sim.vel_list[-1]

        target = self.env.target_pos

        loss = Scalar(0)

        if self.dis_typ == 'L1':
            loss += calc_abs(pos[1] - target[1])
        else:
            loss += calc_sq(pos[1] - target[1])

        print('vel:', vel[1])
        if vel[1].val > -20:
            # de bas à haut
            loss += (vel[1] + Scalar(20)) * self.coeff_dir

        return loss

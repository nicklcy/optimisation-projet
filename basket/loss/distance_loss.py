from basket.loss.loss import Loss

class DistanceLoss(Loss):
    def get_loss(self, tap_times: list[float]):
        self.sim.reset(tap_times=tap_times)
        self.sim.sim_to_target()

        pos = self.sim.pos_list[-1]

        target = self.env.target_pos

        return (pos[1] - target[1]) * (pos[1] - target[1])

from basket.optimizer.optimizer import Optimizer
from basket.scalar import Scalar
from basket.utils.maths import calc_sq, calc_sum

class BGDOptimizer(Optimizer):
    def __init__(self, lr: float, eps: float):
        super().__init__()

        self.lr = float(lr)
        self.eps = float(eps)

    def optim(self, tap_times: list[float], loss: Scalar):
        self.clip_loss(loss)

        diff = loss.grad * self.lr
        flag = False

        if calc_sum(calc_sq(diff.val)) < self.eps:
            flag = True

        for i in range(len(tap_times)):
            tap_times[i] -= diff.val[i]

        tap_times = self.make_tap_times_valid(tap_times)

        return flag

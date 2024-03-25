from basket.optimizer.optimizer import Optimizer
from basket.scalar import Scalar
from basket.utils.maths import calc_norm_2

class BGDOptimizer(Optimizer):
    def __init__(self, lr: float, eps: float):
        super().__init__()

        self.lr = float(lr)
        self.eps = float(eps)

    def optim(self, tap_times: list[float], loss: Scalar):
        diff = loss.grad * self.lr
        if calc_norm_2(diff.val) < self.eps:
            return True

        for i in range(len(tap_times)):
            if i < len(diff.val):
                tap_times[i] -= diff.val[i]
            else:
                tap_times[i] -= 0.01

        tap_times = self.make_tap_times_valid(tap_times)

        return False

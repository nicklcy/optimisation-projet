from basket.optimizer.optimizer import Optimizer
from basket.scalar import Scalar, GradArray
from basket.utils.maths import calc_sq, calc_sum

class AdamOptimizer(Optimizer):
    def __init__(self, lr: float = 1e-3,
                 beta1: float = 0.9,
                 beta2: float = 0.99,
                 eps: float = 1e-8,
                 weight_decay: float = 0,
                 eps_grad: float = 1e-6):
        super().__init__()

        self.lr = float(lr)
        self.beta1 = float(beta1)
        self.beta2 = float(beta2)
        self.eps = float(eps)
        self.weight_decay = float(weight_decay)

        self.eps_grad = float(eps_grad)

        self.m0 = GradArray()
        self.v0 = GradArray()
        self.t = 0

    def optim(self, tap_times: list[float], loss: Scalar):
        self.clip_loss(loss)

        self.t += 1

        g = loss.grad

        g2 = GradArray(g.size)
        for i in range(g.size):
            g2.val[i] = g.val[i] ** 2

        m1 = self.m0 * self.beta1 + g * (1 - self.beta1)
        m1 *= 1 / (1 - self.beta1 ** self.t)
        v1 = self.v0 * self.beta2 + g2 * (1 - self.beta2)
        v1 *= 1 / (1 - self.beta2 ** self.t)


        diff = m1 * self.lr
        for i in range(m1.size):
            diff.val[i] /= (v1.val[i] ** .5 + self.eps)

        flag = False

        if calc_sum(calc_sq(diff.val)) < self.eps_grad:
            flag = True

        for i in range(len(tap_times)):
            tap_times[i] -= diff.val[i]

        tap_times = self.make_tap_times_valid(tap_times)

        self.m0 = m1.clone()
        self.v0 = v1.clone()

        return flag

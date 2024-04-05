from basket.scalar import Scalar
from basket.utils.yaml import read_yaml_file

class Optimizer:
    def __init__(self):
        pass

    def clip_loss(self, loss: Scalar, max_abs_value: float = 5000):
        loss.grad.clip(max_abs_value)

    def optim(self, tap_times: list[float], loss: Scalar):
        raise NotImplementedError

    def make_tap_times_valid(self, arr: list[float]):
        l = len(arr)
        for i in range(l):
            for j in range(i + 1, l):
                if arr[i] > arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
        for i in range(l):
            if arr[i] < 0: arr[i] = 0

from collections.abc import Iterable
from typing import Union
from copy import deepcopy
import functools


class GradArray:
    def __init__(self, len: Union[int, Iterable] = 0):
        if isinstance(len, Iterable):
            self.val = list(deepcopy(len))
        else:
            self.val = [0.] * len

    def resize(self, new_len=0):
        if new_len > len(self.val):
            self.val += [0.] * (new_len - len(self.val))

    def __len__(self):
        return len(self.val)

    @property
    def size(self):
        return len(self)

    def clone(self):
        return deepcopy(self)

    def __add__(self, arr):
        ret = self.clone()
        ret.resize(arr.size)
        for i in range(arr.size):
            ret.val[i] += arr.val[i]
        return ret

    def __mul__(self, k: float):
        ret = self.clone()
        for i in range(self.size):
            ret.val[i] *= k
        return ret

    def __sub__(self, arr):
        return self + arr * (-1)

    def __repr__(self):
        return repr(self.val)


@functools.total_ordering
class Scalar:
    def __init__(self, val: float = 0, grad=None, grad_len=0):
        if isinstance(val, Scalar):
            self.val = val.val
            self.grad = deepcopy(val.grad)
        else:
            self.val = val
            if grad is not None:
                self.grad = grad
            else:
                self.grad = GradArray(grad_len)

    def clone(self):
        return deepcopy(self)

    def __repr__(self):
        return 'Scalar({}, {})'.format(self.val, self.grad)

    def __add__(self, scalar):
        return Scalar(val=self.val + Scalar.get_val(scalar),
                      grad=self.grad + Scalar.get_grad(scalar))

    def __sub__(self, scalar):
        return Scalar(val=self.val - Scalar.get_val(scalar),
                      grad=self.grad - Scalar.get_grad(scalar))

    def __mul__(self, scalar):
        return Scalar(val=self.val * Scalar.get_val(scalar),
                      grad=self.grad * Scalar.get_val(scalar) + Scalar.get_grad(scalar) * self.val)

    def __truediv__(self, scalar):
        sca_val, sca_grad = Scalar.get_val(scalar), scalar.get_grad(scalar)
        return Scalar(val=self.val / sca_val,
                      grad=(self.grad * sca_val - sca_grad * self.val) * (1 / (sca_val ** 2)))

    def __eq__(self, scalar):
        return self.val == Scalar.get_val(scalar)

    def __lt__(self, scalar):
        return self.val < Scalar.get_val(scalar)

    @staticmethod
    def create_grad_1(val: float = 0, id: int = 0):
        grad = GradArray([0] * id + [1])
        return Scalar(val, grad=grad)

    @staticmethod
    def get_val(scalar):
        return scalar.val if isinstance(scalar, Scalar) else scalar

    @staticmethod
    def get_grad(scalar):
        return scalar.grad if isinstance(scalar, Scalar) else GradArray()

    @staticmethod
    def to_scalar_iterable(arr: Iterable):
        res = []
        for ele in arr:
            if isinstance(ele, Iterable):
                res.append(Scalar.to_scalar_iterable(ele))
            else:
                res.append(Scalar(ele))
        return type(arr)(res)

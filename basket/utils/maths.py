from collections.abc import Iterable, Callable
from typing import Union
import math

from basket.scalar import Scalar

scalar_type = Union[Scalar, float]
scalar_arr_type = Union[scalar_type, Iterable[scalar_type]]


def process_arr(process_scalar: Callable, merge_arr: Callable,
                arr: scalar_arr_type):
    if isinstance(arr, Iterable):
        res = []
        for ele in arr:
            res.append(process_arr(process_scalar, merge_arr, ele))
        return merge_arr(res)
    else:
        return process_scalar(arr)


def calc_scalar_abs(num: scalar_type):
    if isinstance(num, Scalar):
        return num if num.val >= 0 else Scalar(0) - num
    else:
        return abs(num)


def calc_abs(arr: scalar_arr_type) -> scalar_arr_type:
    return process_arr(calc_scalar_abs, lambda l: type(arr)(l), arr)


def calc_scalar_sq(num: scalar_type):
    return num * num


def calc_sq(arr: scalar_arr_type) -> scalar_arr_type:
    return process_arr(calc_scalar_sq, lambda l: type(arr)(l), arr)


def calc_sum(arr: Union[scalar_type, Iterable[scalar_type]]) -> scalar_type:
    return process_arr(lambda x: x, lambda l: sum(l, start=Scalar(0)), arr)


def calc_sq_sum(arr: scalar_arr_type) -> scalar_type:
    return calc_sum(calc_sq(arr))


def calc_sqrt(x: scalar_type) -> scalar_type:
    val = math.sqrt(Scalar.get_val(x))
    if isinstance(x, Scalar):
        return Scalar(val=val, grad=x.grad * (1 / 2 / val))
    else:
        return val


def sin(x: scalar_type) -> scalar_type:
    val = math.sin(Scalar.get_val(x))
    if isinstance(x, Scalar):
        return Scalar(val=val, grad=x.grad * math.cos(Scalar.get_val(x)))
    else:
        return val


def cos(x: scalar_type) -> scalar_type:
    val = math.cos(Scalar.get_val(x))
    if isinstance(x, Scalar):
        return Scalar(val=val, grad=x.grad * (-math.sin(Scalar.get_val(x))))
    else:
        return val


def arctan(x: scalar_type) -> scalar_type:
    val = math.atan(Scalar.get_val(x))
    if isinstance(x, Scalar):
        return Scalar(val=val, grad=x.grad * (1 /(x.val**2+1)))
    else:
        return val


def arctan2(y: scalar_type, x: scalar_type) -> scalar_type:
    if abs(Scalar.get_val(x)) < 1e-5:
        val = math.pi / 2 if Scalar.get_val(y) > 0 else -math.pi / 2
        if isinstance(x, Scalar) or isinstance(y, Scalar):
            grad = Scalar.get_grad(x) * (-1 / Scalar.get_val(y))
            return Scalar(val=val, grad=grad)
        else:
            return val
    elif abs(Scalar.get_val(y)) < 1e-5:
        val = 0 if Scalar.get_val(x) > 0 else -math.pi
        if isinstance(x, Scalar) or isinstance(y, Scalar):
            grad = Scalar.get_grad(y) * (1 / Scalar.get_val(x))
            return Scalar(val=val, grad=grad)
        else:
            return val
    else:
        if isinstance(x, Scalar) or isinstance(y, Scalar):
            x, y = Scalar(x), Scalar(y)
        res = arctan(y / x)
        if Scalar.get_val(x) < 0:
            res += math.pi
        return res

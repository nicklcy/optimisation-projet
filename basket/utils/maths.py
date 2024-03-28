from collections.abc import Iterable, Callable
from typing import Union

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
    return process_arr(lambda x: x, sum, arr)

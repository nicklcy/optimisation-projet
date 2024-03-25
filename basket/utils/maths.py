from collections.abc import Iterable
from typing import Union

from basket.scalar import Scalar

scalar_type = Union[Scalar, float]

def calc_abs(num: scalar_type):
    if isinstance(num, Scalar):
        return num if num.val >= 0 else Scalar(0) - num
    else:
        return abs(num)


def calc_norm_2(num: Union[scalar_type, Iterable[scalar_type]]) -> scalar_type:
    if isinstance(num, Iterable):
        sum = None
        for ele in num:
            if sum is None:
                sum = type(ele)(0)
            sum += calc_norm_2(ele)
        return sum
    else:
        return num * num

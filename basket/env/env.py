from typing import Tuple

from basket.scalar import Scalar

Coor = Tuple[float, float]


class Env:
    def __init__(self,
                 init_pos: Coor, target_pos: Coor, init_vel: Coor,
                 gravity: Coor, bounds: Tuple[Coor, Coor],
                 tap_vel: float, min_tap_interval):
        self.init_pos = Scalar.to_scalar_iterable(init_pos)
        self.target_pos = Scalar.to_scalar_iterable(target_pos)
        self.init_vel = Scalar.to_scalar_iterable(init_vel)
        self.gravity = Scalar.to_scalar_iterable(gravity)
        self.bounds = Scalar.to_scalar_iterable(bounds)
        self.tap_vel = Scalar(tap_vel)
        self.min_tap_interval = min_tap_interval

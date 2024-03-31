from typing import Tuple

from basket.scalar import Scalar

Coor = Tuple[float, float]


class Env:
    def __init__(self,
                 init_pos: Coor,
                 target_pos: Coor,
                 init_vel: Coor,
                 gravity: Coor,
                 bounds: Tuple[Coor, Coor],
                 tap_vel: float,
                 min_tap_interval: float,
                 ball_radius: float,
                 ground_threshold: float,
                 basket_radius: float,
                 basket_ring_radius: float,
                 coeff_bounce: float = 0,
                 air_friction: float = 0,
                 board_width: float = 0,
                 board_height: float = 0):

        self.init_pos = Scalar.to_scalar_iterable(init_pos)
        self.target_pos = Scalar.to_scalar_iterable(target_pos)
        self.init_vel = Scalar.to_scalar_iterable(init_vel)
        self.gravity = Scalar.to_scalar_iterable(gravity)
        self.bounds = Scalar.to_scalar_iterable(bounds)
        self.tap_vel = Scalar(tap_vel)
        self.min_tap_interval = min_tap_interval
        self.ball_radius = Scalar(ball_radius)
        self.ground_threshold = Scalar(ground_threshold)
        self.basket_radius = Scalar(basket_radius)
        self.basket_ring_radius = Scalar(basket_ring_radius)
        self.coeff_bounce = Scalar(coeff_bounce)
        self.air_friction = Scalar(air_friction)
        self.board_width = Scalar(board_width)
        self.board_height = Scalar(board_height)

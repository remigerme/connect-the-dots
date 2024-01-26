from enum import Enum
from typing import Optional

from points import Point, add, mul, norm


class DotLabelMode(Enum):
    AUTO = 1
    MANUAL = 2

class DotLabel:
    def __init__(
            self,
            mode: DotLabelMode = DotLabelMode.AUTO,
            x: Optional[float] = None,
            y: Optional[float] = None):
        self.mode = mode
        self.x = x
        self.y = y
    
    def set_manually_to(self, x: float, y: float):
        self.mode = DotLabelMode.MANUAL
        self.x = x
        self.y = y

    def set_auto(self):
        self.mode = DotLabelMode.AUTO
        self.x = None
        self.y = None

    def get_position(self, a: Point, b: Point, c: Point, radius: float) -> Point:
        if self.mode == DotLabelMode.MANUAL:
            return (self.x, self.y)
        return DotLabel.place_label(a, b, c, radius)
    
    @staticmethod
    def place_label_auto(a: Point, b: Point, c: Point, radius: float) -> Point:
        epsilon = 1e-5 # magic trick to handle first and colinear points
        ab = add(b, mul(a, -1))
        ab = mul(ab, 1 / (norm(ab) + epsilon))
        cb = add(b, mul(c, -1))
        cb = mul(cb, 1 / (norm(cb) + epsilon))
        v = add(ab, cb)
        v = mul(v, radius / (norm(v) + epsilon))
        return add(b, v)

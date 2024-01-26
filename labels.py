from enum import Enum

from points import Point, add, mul, norm


class LabelMode(Enum):
    AUTO = 1
    MANUAL = 2

class Label:
    def __init__(self):
        self.mode = LabelMode
        self.x = None
        self.y = None
    
    def set_manually_to(self, x: float, y: float):
        self.mode = LabelMode.MANUAL
        self.x = x
        self.y = y

    def set_auto(self):
        self.mode = LabelMode.AUTO
        self.x = None
        self.y = None

    def get_position(self, a: Point, b: Point, c: Point, radius: float) -> Point:
        if self.mode == LabelMode.MANUAL:
            return (self.x, self.y)
        return Label.place_label(a, b, c, radius)
    
    def place_label(a: Point, b: Point, c: Point, radius: float) -> Point:
        epsilon = 1e-5 # magic trick to handle first and colinear points
        ab = add(b, mul(a, -1))
        ab = mul(ab, 1 / (norm(ab) + epsilon))
        cb = add(b, mul(c, -1))
        cb = mul(cb, 1 / (norm(cb) + epsilon))
        v = add(ab, cb)
        v = mul(v, radius / (norm(v) + epsilon))
        return add(b, v)

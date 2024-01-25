from random import random
from math import cos, sin, pi, sqrt

from constants import RGBColor
from points import Point, add, mul, norm

def get_opposite_color(color: RGBColor) -> RGBColor:
    return (255 - color[0], 255 - color[1], 255 - color[2])

def rgb_to_hex_string(color: RGBColor) -> str:
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

def random_point_on_circle(center: Point, radius: float) -> Point:
    angle = random() * 2 * pi
    x = center[0] + radius * cos(angle)
    y = center[1] + radius * sin(angle)
    return (x, y)

def place_label(
        a: Point,
        b: Point,
        c: Point,
        radius: float) -> Point:
    epsilon = 1e-5 # magic trick to handle first and colinear points
    ab = add(b, mul(a, -1))
    ab = mul(ab, 1 / (norm(ab) + epsilon))
    cb = add(b, mul(c, -1))
    cb = mul(cb, 1 / (norm(cb) + epsilon))
    v = add(ab, cb)
    v = mul(v, radius / (norm(v) + epsilon))
    return add(b, v)

from random import random
from math import cos, sin, pi

from constants import RGBColor

def get_opposite_color(color: RGBColor) -> RGBColor:
    return (255 - color[0], 255 - color[1], 255 - color[2])

def rgb_to_hex_string(color: RGBColor) -> str:
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

def random_point_on_circle(center: tuple[float, float], radius: float) -> tuple[int, int]:
    angle = random() * 2 * pi
    x = center[0] + radius * cos(angle)
    y = center[1] + radius * sin(angle)
    return (x, y)

from math import sqrt

Point = tuple[float, float]

def add(pa: Point, pb: Point) -> Point:
    return (pa[0] + pb[0], pa[1] + pb[1])

def mul(p: Point, l: float) -> Point:
    return (l * p[0], l * p[1])

def norm(p: Point) -> float:
    return sqrt(p[0] ** 2 + p[1] ** 2)

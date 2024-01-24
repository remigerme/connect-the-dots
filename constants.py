from enum import Enum

RGBColor = tuple[int, int, int]

DOT_WIDTH = 10
RADIUS_LABEL = 25
BLACK: RGBColor = (0, 0, 0)
RED: RGBColor = (255, 0, 0)
GREEN: RGBColor = (0, 255, 0)
BLUE: RGBColor = (0, 0, 255)
WHITE: RGBColor = (255, 255, 255)

class AppMode(Enum):
    ADD = 1
    EDIT = 2
    DEL = 3

MODE_LABEL_INFO: dict[AppMode, tuple[str, RGBColor]] = {
    AppMode.ADD: ("Mode actuel : ajout de points", GREEN),
    AppMode.EDIT: ("Mode actuel : sélection de points", BLUE),
    AppMode.DEL: ("Mode actuel : suppression de points", RED)
}

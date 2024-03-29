from enum import Enum

HELP = [
    "On note A/D pour activer / désactiver :",
    "<espace> pour A/D mode sélection",
    "drag and drop possible des labels en mode sélection",
    "<r> pour renuméroter un point sélectionné",
    "<esc> pour A/D mode suppression",
    "<i> pour A/D l'image d'arrière-plan",
    "<n> pour A/D les labels des points",
    "<s> pour enregistrer l'image des points à relier générée",
    "<t> pour A/D les traits entre les points",
]

RGBColor = tuple[int, int, int]

DOT_WIDTH = 8
LABEL_RADIUS = 12
FONT_SIZE = 10
MARGIN_UP_WINDOW = 5
BLACK: RGBColor = (0, 0, 0)
RED: RGBColor = (255, 0, 0)
GREEN: RGBColor = (0, 255, 0)
BLUE: RGBColor = (0, 0, 255)
CYAN: RGBColor = (0, 255, 255)
WHITE: RGBColor = (255, 255, 255)


class AppMode(Enum):
    ADD = 1
    EDIT = 2
    DEL = 3


MODE_LABEL_INFO: dict[AppMode, tuple[str, RGBColor]] = {
    AppMode.ADD: ("Mode actuel : ajout de points", GREEN),
    AppMode.EDIT: ("Mode actuel : sélection de points", CYAN),
    AppMode.DEL: ("Mode actuel : suppression de points", RED),
}

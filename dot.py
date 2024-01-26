from typing import Optional

from dotlabel import DotLabel

class Dot:
    id = 0
    
    def __init__(self, x: float, y: float):
        self.id = Dot.id
        Dot.id += 1
        self.tag = f"dot-{self.id}"
        self.x = x
        self.y = y
        self.label = DotLabel()

    def set_coordinates(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def draw(self,
             canvas,
             width: float,
             dot_color: str,
             label_status: bool,
             before: Optional["Dot"],
             after: Optional["Dot"],
             label_radius: Optional[float],
             i: Optional[int],
             label_color: Optional[str]):
        canvas.create_oval(
            self.x - width / 2,
            self.y - width / 2,
            self.x + width / 2,
            self.y + width / 2,
            fill=dot_color,
            tag=self.tag
        )
        if label_status:
            a = (before.x, before.y)
            b = (self.x, self.y)
            c = (after.x, after.y)
            self.label.draw(canvas, a, b, c, label_radius, str(i), label_color)

    def erase(self, canvas):
        canvas.delete(self.tag)
        self.label.erase(canvas)

    def update(self,
             canvas,
             width: float,
             dot_color: str,
             label_status: bool,
             before: Optional["Dot"],
             after: Optional["Dot"],
             label_radius: Optional[float],
             i: Optional[int],
             label_color: Optional[str]):
        self.erase(canvas)
        self.label.erase(canvas)
        self.draw(
            canvas,
            width,
            dot_color,
            label_status,
            before,
            after,
            label_radius,
            i,
            label_color
        )

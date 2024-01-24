import sys
from enum import Enum
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Tk, Canvas, Label, simpledialog
from random import random
from math import cos, sin, pi


DOT_WIDTH = 10
FONT_SIZE = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class AppMode(Enum):
    ADD = 1
    EDIT = 2
    DEL = 3

MODE_LABEL_INFO = {
    AppMode.ADD: ("Mode actuel : ajout de points", GREEN),
    AppMode.EDIT: ("Mode actuel : sélection de points", BLUE),
    AppMode.DEL: ("Mode actuel : suppression de points", RED)
}

def get_opposite_color(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return (255 - color[0], 255 - color[1], 255 - color[2])

def rgb_to_hex_string(color: tuple[int, int, int]) -> str:
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"

def random_point_on_circle(center: tuple[float, float], radius: float) -> tuple[int, int]:
    angle = random() * 2 * pi
    x = center[0] + radius * cos(angle)
    y = center[1] + radius * sin(angle)
    return (x, y)

class App:
    def __init__(self, filename):
        self.root = Tk()
    
        def compute_size(W: int, H: int):
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            f = min(sw / W, sh / H)
            self.W = int(0.8 * f * W)
            self.H = int(0.8 * f * H)

        with Image.open(filename) as im:
            (W, H) = im.size
            compute_size(W, H)
            im = im.resize((self.W, self.H))
            self.filename = f"dotwork.{filename}"
            im.save(self.filename)
            self.img = im

        self.points = []
        self.selected = set()
        self.status_labels = True
        self.mode = AppMode.ADD
        self.i_tag = 0

        #Bindings 
        self.root.bind("<Button-1>", self.handle_dot)
        self.root.bind("<space>", self.toggle_edit_mode)
        self.root.bind("<Escape>", self.toggle_del_mode)
        self.root.bind("<KeyPress-i>", self.toggle_image)
        self.root.bind("<KeyPress-n>", self.toggle_labels)
        self.root.bind("<KeyPress-s>", self.save_image)
        self.root.bind("<KeyPress-r>", self.renumber)

        # Mode bar info
        self.mode_label = Label(self.root)
        self.mode_label.pack()
        self.update_mode_label()

        # Canvas
        self.canvas = Canvas(self.root, width=self.W, height=self.H)
        self.canvas.pack()
        self.tk_img = ImageTk.PhotoImage(file=self.filename)
        self.canvas.create_image(self.W / 2, self.H / 2, image=self.tk_img, tag="bg_img")
        self.status_bg_img = True
    
    def run(self):
        self.root.mainloop()

    def update_mode_label(self):
        (text, rgb_color) = MODE_LABEL_INFO[self.mode]
        self.mode_label.config(
            text = text,
            bg = rgb_to_hex_string(rgb_color)
        )

    def toggle_edit_mode(self, event):
        if self.mode == AppMode.EDIT:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.EDIT
        self.update_mode_label()
    
    def toggle_del_mode(self, event):
        if self.mode == AppMode.DEL:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.DEL
        self.update_mode_label()
    
    def create_dot(self, x: float, y: float, tag: str, color=BLACK):
        self.canvas.create_oval(x, y, x + DOT_WIDTH, y + DOT_WIDTH, fill=rgb_to_hex_string(color), tag=tag)

    def create_label(self, x: float, y: float, i: int, color=BLACK):
        tag = ("label", f"label-{i}")
        self.canvas.create_text(x + DOT_WIDTH / 2, y - 2 * DOT_WIDTH, text=f"{i}", fill=rgb_to_hex_string(color), tag=tag)

    def create_label_with_check(self, x: float, y: float, i: int, color=BLACK):
        if self.status_labels:
            tag = ("label", f"label-{i}")
            self.canvas.create_text(x + DOT_WIDTH / 2, y - 2 * DOT_WIDTH, text=f"{i}", fill=rgb_to_hex_string(color), tag=tag)

    def show_labels(self):
        self.canvas.delete("label")
        for (i, (x, y, _)) in enumerate(self.points):
            self.create_label(x, y, i + 1)

    def clear_dots(self):
        for (_, _, tag) in self.points:
            self.canvas.delete(tag)
    
    def redraw_dots(self):
        self.clear_dots() # do it first to avoid concurrential changes
        for (i, (x, y, _)) in enumerate(self.points):
            color = BLUE if i in self.selected else BLACK
            self.create_dot(x, y, f"dot-{i}", color)

    def toggle_image(self, event):
        if self.status_bg_img:
            self.canvas.delete("bg_img")
        else:
            self.canvas.create_image(self.W / 2, self.H / 2, image=self.tk_img, tag="bg_img")
            # Dégeu mais l'image repasse au premier plan
            # On delete et redraw tous les points
            self.canvas.delete("label")
            for (i, (x, y, tag)) in enumerate(self.points):
                self.canvas.delete(tag)
                self.create_dot(x, y, tag)
                self.create_label_with_check(x, y, i + 1)
        self.status_bg_img = not self.status_bg_img
    
    def toggle_labels(self, event):
        if self.status_labels:
            self.canvas.delete("label")
        else:
            self.show_labels()
        self.status_labels = not self.status_labels
    
    def toggle_select(self, i: int):
        (x, y, tag) = self.points[i]
        self.canvas.delete(tag)
        if i in self.selected:
            self.create_dot(x, y, tag)
            self.selected.remove(i)
        else:
            self.create_dot(x, y, tag, BLUE)
            self.selected.add(i)

    def save_image(self, event):
        im = Image.new(mode="RGB", size=(self.W, self.H), color=WHITE)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(r"arial.ttf", FONT_SIZE)
        # Draw points
        for (i, (x, y, _)) in enumerate(self.points):
            draw.ellipse((x, y, x + DOT_WIDTH, y + DOT_WIDTH), fill=BLACK, outline=BLACK)
            draw.text(random_point_on_circle((x, y), FONT_SIZE), str(i + 1), fill=BLACK, font=font)
        im.save(f"connect-the-dots-{self.filename}")

    def handle_dot(self, event):
        (x, y) = (event.x, event.y)
        if y < 10:
            return
        if self.mode == AppMode.ADD:
            self.add_dot(x, y)
        elif self.mode == AppMode.DEL:
            self.remove_dot(x, y)
        elif self.mode == AppMode.EDIT:
            self.edit_dot(x, y)
        else:
            print("Error : unknown mode")

    def add_dot(self, x: float, y: float):
        tag = f"dot-{self.i_tag}"
        self.i_tag += 1
        self.points.append((x, y, tag))
        self.create_dot(x, y, tag)
        self.create_label_with_check(x, y, len(self.points))

    def edit_dot(self, x: float, y: float):
        n = self.find_closest_dot(x, y)
        (x_, y_, _) = self.points[n]
        if (x - x_) ** 2 + (y - y_) ** 2 < (4 * DOT_WIDTH) ** 2:
            self.toggle_select(n)

    def find_closest_dot(self, x: float, y: float) -> int:
        def d(x_, y_):
            return (x - x_) ** 2 + (y - y_) ** 2
        n = 0
        d_min = 10e9
        for (i, (x_, y_, _)) in enumerate(self.points):
            if d(x_, y_) < d_min:
                n = i
                d_min = d(x_, y_)
        return n

    def remove_dot(self, x: float, y: float):
        n = self.find_closest_dot(x, y)
        (_, _, tag) = self.points.pop(n)
        self.canvas.delete(tag)
        label_tag = f"label-{n + 1}"
        self.canvas.delete(label_tag)
        if self.status_labels:
            self.show_labels()
    
    def renumber(self, event):
        if len(self.selected) == 0:
            raise Exception("Select a point to renumber.")
        if len(self.selected) >= 2:
            raise Exception("Can't renumber multiple points at once.")
        n = list(self.selected)[0]
        new_n = simpledialog.askinteger("Renumérotation", "Nouveau numéro : ")
        if new_n is not None and 1 <= new_n <= len(self.points):
            self.selected.remove(n)
            self.points.insert(new_n - 1, self.points.pop(n))
            self.redraw_dots()
            if self.status_labels:
                self.show_labels()

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        raise Exception("Missing file in command line argument.")
    
    filename = args[0]
    app = App(filename)
    app.run()


if __name__ == "__main__":
    main()

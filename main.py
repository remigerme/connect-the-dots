import sys
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Tk, Canvas, Label, Button, Toplevel, simpledialog

from constants import *
from dot import Dot
from utils import rgb_to_hex_string
from dragmanager import DragManager

# Decorators used to update various things
def update_mode_label(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.apply_update_mode_label()
        return result
    return wrapper

def update_dots(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.apply_update_dots()
        return result
    return wrapper


class App:

    @update_mode_label
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

        self.dots: list[Dot] = []
        self.selected: set[Dot] = set()
        self.labels_status = True
        self.mode = AppMode.ADD

        # Help panel
        self.help_button = Button(self.root, text="Aide", command=self.show_help_window)
        self.help_button.grid(row=0, column=1)

        # Mode bar info
        self.mode_label = Label(self.root)
        self.mode_label.grid(row=0, column=0)

        # Canvas
        self.canvas = Canvas(self.root, width=self.W, height=self.H)
        self.canvas.grid(columnspan=2)
        self.tk_img = ImageTk.PhotoImage(file=self.filename)
        self.canvas.create_image(self.W / 2, self.H / 2, image=self.tk_img, tag="bg_img")
        self.status_bg_img = True

        #Bindings 
        self.canvas.bind("<Button-1>", self.handle_dot)
        self.root.bind("<space>", self.toggle_edit_mode)
        self.root.bind("<Escape>", self.toggle_del_mode)
        self.root.bind("<KeyPress-i>", self.toggle_image)
        self.root.bind("<KeyPress-n>", self.toggle_labels)
        self.root.bind("<KeyPress-s>", self.save_image)
        self.root.bind("<KeyPress-r>", self.renumber)

        # Drag and drop
        self.root.bind("<ButtonPress-1>", self.drag_on_start)
        self.root.bind("<B1-Motion>", self.drag_on_drag)
        self.root.bind("<ButtonRelease-1>", self.drag_on_drop)
    
    def run(self):
        self.root.mainloop()

    def drag_on_start(self, event):
        ...

    def drag_on_drag(self, event):
        ...
    
    def drag_on_drop(self, event):
        ...

    def show_help_window(self):
        top = Toplevel()
        top.title("Aide")
        for h in HELP:
            Label(top, text=h, padx=30, pady=10).pack()

    @update_mode_label
    def toggle_edit_mode(self, event):
        if self.mode == AppMode.EDIT:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.EDIT
    
    @update_mode_label
    def toggle_del_mode(self, event):
        if self.mode == AppMode.DEL:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.DEL

    @update_dots
    def toggle_image(self, event):
        if self.status_bg_img:
            self.canvas.delete("bg_img")
        else:
            self.canvas.create_image(self.W / 2, self.H / 2, image=self.tk_img, tag="bg_img")
        self.status_bg_img = not self.status_bg_img
    
    @update_dots
    def toggle_labels(self, event):
        self.labels_status = not self.labels_status
    
    @update_dots
    def toggle_select(self, i: int):
        if i in self.selected:
            self.selected.remove(i)
        else:
            self.selected.add(i)

    def save_image(self, event):
        im = Image.new(mode="RGB", size=(self.W, self.H), color=WHITE)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(r"arial.ttf", FONT_SIZE)
        # Draw points
        for (i, dot) in enumerate(self.dots):
            draw.ellipse(
                (dot.x - DOT_WIDTH / 2,
                 dot.y - DOT_WIDTH / 2,
                 dot.x + DOT_WIDTH / 2,
                 dot.y + DOT_WIDTH / 2),
                fill=BLACK,
                outline=BLACK)
            n = len(self.dots)
            a = self.dots[(i - 1) % n]
            c = self.dots[(i + 1) % n]
            (x, y) = dot.label.get_position((a.x, a.y), (dot.x, dot.y), (c.x, c.y), LABEL_RADIUS_PIL)
            draw.text(
                (x, y),
                str(i + 1),
                fill=BLACK,
                anchor="mm",
                font=font)
        im.save(f"connect-the-dots-{self.filename}")

    def handle_dot(self, event):
        (x, y) = (event.x, event.y)
        if y < MARGIN_UP_WINDOW:
            return
        if self.mode == AppMode.ADD:
            self.add_dot(x, y)
        elif self.mode == AppMode.DEL:
            self.remove_dot(x, y)
        elif self.mode == AppMode.EDIT:
            self.edit_dot(x, y)
        else:
            print("Error : unknown mode")

    @update_dots
    def add_dot(self, x: float, y: float):
        self.dots.append(Dot(x, y))

    def edit_dot(self, x: float, y: float):
        n = self.find_closest_dot(x, y)
        (x_, y_, _) = self.dots[n]
        if (x - x_) ** 2 + (y - y_) ** 2 < (4 * DOT_WIDTH) ** 2:
            self.toggle_select(n)

    def find_closest_dot(self, x: float, y: float) -> int:
        def d(x_, y_):
            return (x - x_) ** 2 + (y - y_) ** 2
        n = 0
        d_min = 10e9
        for (i, dot) in enumerate(self.dots):
            if d(dot.x, dot.y) < d_min:
                n = i
                d_min = d(dot.x, dot.y)
        return n

    @update_dots
    def remove_dot(self, x: float, y: float):
        n = self.find_closest_dot(x, y)
        dot = self.dots[n]
        if (x - self.dot.x) ** 2 + (y - self.dot.y) ** 2 < (4 * DOT_WIDTH) ** 2:
            dot.erase()
            self.dots.pop(n)

    @update_dots
    def renumber(self, event):
        if len(self.selected) == 0:
            raise Exception("Select a point to renumber.")
        if len(self.selected) >= 2:
            raise Exception("Can't renumber multiple points at once.")
        n = list(self.selected)[0]
        new_n = simpledialog.askinteger("Renumérotation", "Nouveau numéro : ")
        if new_n is not None and 1 <= new_n <= len(self.points):
            self.selected.remove(n)
            self.dots.insert(new_n - 1, self.dots.pop(n))

    def apply_update_mode_label(self):
        (text, rgb_color) = MODE_LABEL_INFO[self.mode]
        self.mode_label.config(
            text = text,
            bg = rgb_to_hex_string(rgb_color)
        )
    
    def apply_update_dots(self):
        n = len(self.dots)
        for dot in self.dots:
            dot.erase(self.canvas)
        for (i, dot) in enumerate(self.dots):
            dot.draw(
                self.canvas,
                DOT_WIDTH,
                rgb_to_hex_string(BLUE if i in self.selected else BLACK),
                self.labels_status,
                self.dots[(i - 1) % n],
                self.dots[(i + 1) % n],
                LABEL_RADIUS_TKINTER,
                i + 1,
                rgb_to_hex_string(BLACK)
            )


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        raise Exception("Missing file in command line argument.")
    
    filename = args[0]
    app = App(filename)
    app.run()


if __name__ == "__main__":
    main()

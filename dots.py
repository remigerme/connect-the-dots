import sys
from enum import Enum
from PIL import Image, ImageTk
from tkinter import Tk, Canvas


DOT_WIDTH = 5


class AppMode(Enum):
    ADD = 1
    EDIT = 2
    DEL = 3


class App:
    def __init__(self, filename):
        self.root = Tk()
    
        def compute_size(W: int, H: int):
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            f = min(sw / W, sh / H)
            self.W = int(0.9 * f * W)
            self.H = int(0.9 * f * H)

        with Image.open(filename) as im:
            (W, H) = im.size
            compute_size(W, H)
            im = im.resize((self.W, self.H))
            self.filename = f"dotwork.{filename}"
            im.save(self.filename)

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

        self.canvas = Canvas(self.root, width=self.W, height=self.H)
        self.canvas.pack()
        self.img = ImageTk.PhotoImage(file=self.filename)
        self.canvas.create_image(self.W / 2, self.H / 2, image=self.img, tag="bg_img")
        self.status_bg_img = True
    
    def run(self):
        self.root.mainloop()

    def toggle_edit_mode(self, event):
        if self.mode == AppMode.EDIT:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.EDIT
    
    def toggle_del_mode(self, event):
        if self.mode == AppMode.DEL:
            self.mode = AppMode.ADD
        else:
            self.mode = AppMode.DEL
    
    def create_dot(self, x: float, y: float, tag: str, color="black"):
        self.canvas.create_oval(x, y, x + DOT_WIDTH, y + DOT_WIDTH, width=DOT_WIDTH, outline=color, tag=tag)

    def create_label(self, x: float, y: float, i: int):
        tag = ("label", f"label-{i}")
        self.canvas.create_text(x + DOT_WIDTH / 2, y - 2 * DOT_WIDTH, text=f"{i}", fill="black", tag=tag)

    def create_label_with_check(self, x: float, y: float, i: int):
        if self.status_labels:
            tag = ("label", f"label-{i}")
            self.canvas.create_text(x + DOT_WIDTH / 2, y - 2 * DOT_WIDTH, text=f"{i}", fill="black", tag=tag)

    def show_labels(self):
        self.canvas.delete("label")
        for (i, (x, y, _)) in enumerate(self.points):
            self.create_label(x, y, i + 1)

    def toggle_image(self, event):
        if self.status_bg_img:
            self.canvas.delete("bg_img")
        else:
            self.canvas.create_image(self.W / 2, self.H / 2, image=self.img, tag="bg_img")
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
            self.create_dot(x, y, tag, "red")
            self.selected.add(i)

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


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        raise Exception("Missing file in command line argument.")
    
    filename = args[0]
    app = App(filename)
    app.run()


if __name__ == "__main__":
    main()

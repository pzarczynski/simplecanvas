import io
from tkinter import *
from tkinter import colorchooser

from PIL import Image


def input(width, height):
    root = Tk()
    root.title("Canvas")
    window = _Window(root, width, height)

    root.protocol("WM_DELETE_WINDOW", window.exit)
    root.resizable(False, False)
    root.mainloop()

    return window.image


class _Window:
    def __init__(self, master, width, height):
        self.master = master

        self.old_x = None
        self.old_y = None
        self.brush_color = "Black"
        self.brush_width = 10

        self.init_widgets(width, height)

    def draw(self, c):
        if self.old_x and self.old_y:
            self.canvas.create_line(
                self.old_x,
                self.old_y,
                c.x,
                c.y,
                width=self.brush_width,
                fill=self.brush_color,
                capstyle="round",
                smooth=True,
            )

        self.old_x = c.x
        self.old_y = c.y

    def reset(self, c):
        self.old_x = self.old_y = None

    def set_brush_width(self, width):
        self.brush_width = width

    def set_brush_color(self):
        self.brush_color = colorchooser.askcolor(self.brush_color)[1]

    def exit(self):
        ps = self.canvas.postscript(colormode="color")
        self.image = Image.open(io.BytesIO(ps.encode("utf-8")))
        self.master.destroy()

    def clear(self):
        self.canvas.delete(ALL)

    def init_widgets(self, width, height):
        self.controls = Frame(self.master)

        pad = width // 80

        Scale(
            self.controls,
            from_=1,
            to=width // 4,
            showvalue=False,
            command=self.set_brush_width,
            orient="horizontal",
        ).pack(side="left", padx=pad, pady=pad)

        Button(self.controls, text="Pick color", command=self.set_brush_color).pack(
            side="left", padx=pad, pady=pad
        )

        Button(self.controls, text="Clear", command=self.clear).pack(
            side="left", padx=pad, pady=pad
        )

        self.controls.pack(side="bottom")

        self.canvas = Canvas(self.master, width=width, height=height, bg="White")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

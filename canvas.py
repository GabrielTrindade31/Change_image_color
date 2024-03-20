from tkinter import Canvas
from settings import *

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background = CANVAS_BACKGROUND, bd=0, highlightthickness=0, relief='ridge')
        self.grid(column=1, row=0, sticky='nsew', padx=10, pady = 10)
        self.bind('<Configure>', resize_image)

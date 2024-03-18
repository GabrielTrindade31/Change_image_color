import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk


class Menu(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky='nsew')

        # create tabs
        self.add("Import")
        self.add("Edit")
        self.add("Export")

        # Widgets
        # PositionFrame(self.tab('Import'))
        # PositionFrame(self.tab('Edit'))
        # PositionFrame(self.tab('Export'))
        


class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

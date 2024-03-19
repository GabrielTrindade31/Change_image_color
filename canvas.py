import customtkinter as ctk
from tkinter import filedialog, Canvas


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan = 2, row=0, sticky='nsew')
        self.import_func = import_func

        open_image_button = ctk.CTkButton(
            self, text="Open Image", command=self.open_dialog)
        open_image_button.grid(row=0, column=0, padx=20, pady=20)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background = '#232323', bd=0, highlightthickness=0, relief='ridge')
        self.grid(column=1, row=0, sticky='nsew', padx=10, pady = 10)
        self.bind('<Configure>', resize_image)

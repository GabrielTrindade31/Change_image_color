import customtkinter as ctk
from tkinter import filedialog


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#232323')
        self.pack(fill='x', pady=4, ipady=8)


class FileNamePanel(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent=parent)

        self.name_string = name_string
        self.name_string.trace('w', self.update_text)
        self.file_string = file_string

        # check boxes
        ctk.CTkEntry(self, textvariable=self.name_string).pack(
            fill='x', padx=20, pady=5)
        frame = ctk.CTkFrame(self, fg_color='transparent')
        jpg_chk = ctk.CTkCheckBox(frame, text='jpg', variable=self.file_string,
                                  onvalue='jpg', offvalue='png', command=lambda: self.click('jpg'))
        jpg_chk.pack(side='left', fill='x', expand=True)
        png_chk = ctk.CTkCheckBox(frame, text='png', variable=self.file_string,
                                  onvalue='png', offvalue='jpg', command=lambda: self.click('png'))
        png_chk.pack(side='left', fill='x', expand=True)
        frame.pack(expand=True, fill='x', padx=20)

        self.output = ctk.CTkLabel(self, text='')
        self.output.pack()

    def click(self, value):
        self.file_string.set(value)
        self.update_text()

    def update_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get().replace(' ', '_') + '.' + self.file_string.get()
            self.output.configure(text=text)


class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent=parent)
        self.path_string = path_string

        ctk.CTkButton(self, text='Open Explorer',
                      command=lambda: self.open_file_dialog()).pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.path_string).pack(
            expand=True, fill='both', padx=5, pady=5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(master=parent, text='save', command=self.save)
        self.pack(side = 'bottom', pady = 10)

        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(self.name_string.get(),
                          self.file_string.get(),
                          self.path_string.get())

import customtkinter as ctk
import os
from tkinter import filedialog
from settings import *
from canvas import *


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
        self.placeholder = ''
        self.get_download_path()

        ctk.CTkButton(self, text='Open Explorer',
                      command=lambda: self.open_file_dialog()).pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.path_string, placeholder_text=self.placeholder).pack(
            expand=True, fill='both', padx=5, pady=5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())

    def get_download_path(self):
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            self.path_string.set(location)
        else:
            self.path_string.set(os.path.join(
                os.path.expanduser('~'), 'downloads'))


class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(master=parent, text='Save', command=self.save)
        self.pack(side='bottom', pady=10)

        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string

    def save(self):
        self.export_image(self.name_string.get(),
                          self.file_string.get(),
                          self.path_string.get())


class OpenButton(ctk.CTkButton):
    def __init__(self, parent, import_func):
        super().__init__(master=parent, text="Open Image", command=self.open_dialog)
        self.pack(side='top', pady=10)
        self.import_func = import_func
       
    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


class DropdownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_var, options):
        super().__init__(master=parent, values=options, fg_color='#4a4a4a',
                         button_color='#444', button_hover_color='#333', dropdown_fg_color='#666', variable=data_var, command=self.updateChannel)
        self.pack(fill='x', pady=4)

    def updateChannel(self, parent):
        self._variable.set(parent)


class ColorPanel(Panel):
    def __init__(self, parent, r_var, g_var, b_var, a_var, manipulate_image):
        super().__init__(parent=parent)
        self.pack(fill='x', pady=4)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')

        label = ctk.CTkLabel(self, text="R")
        label.grid(column=0, row=0, pady=5, sticky='E')
        r_entry = ctk.CTkEntry(self,  textvariable=r_var)
        r_entry.grid(column=1, row=0, pady=5)
        r_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=r_var)
        r_slider.grid(column=0, row=1, columnspan=2, pady=(0, 10))

        label = ctk.CTkLabel(self, text="G")
        label.grid(column=0, row=2, pady=5, sticky='E')
        g_entry = ctk.CTkEntry(self, textvariable=g_var)
        g_entry.grid(column=1, row=2, pady=5)
        g_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=g_var)
        g_slider.grid(column=0, row=3, columnspan=2, pady=(0, 10))

        label = ctk.CTkLabel(self, text="B")
        label.grid(column=0, row=4, pady=5, sticky='E')
        b_entry = ctk.CTkEntry(self, textvariable=b_var)
        b_entry.grid(column=1, row=4, pady=5)
        b_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=b_var)
        b_slider.grid(column=0, row=5, columnspan=2, pady=(0, 10))

        label = ctk.CTkLabel(self, text="A")
        label.grid(column=0, row=6, pady=5, sticky='E')
        a_entry = ctk.CTkEntry(self, textvariable=a_var)
        a_entry.grid(column=1, row=6, pady=5)
        a_slider = ctk.CTkSlider(self, from_=ALPHA_MIN, to=ALPHA_MAX, width=200, variable=a_var)
        a_slider.grid(column=0, row=7, columnspan=2, pady=(0, 10))

        # Create a button to apply color substitution
        apply_button = ctk.CTkButton(self, text="Apply color", command=manipulate_image)
        apply_button.grid(column=0, row=8, columnspan=2, pady=(0, 10))
    
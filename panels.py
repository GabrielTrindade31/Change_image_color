import customtkinter as ctk
import os
from customtkinter import filedialog
from settings import *
from canvas import *


class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color='#232323')
        self.pack(fill='x', pady=4, ipady=8)


# Import Frame
class OpenButton(ctk.CTkButton):
    def __init__(self, parent, import_func):
        super().__init__(master=parent, text="Open Image", command=self.open_dialog)
        self.pack(side='top', pady=10)
        self.import_func = import_func
       
    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


# Filter Frame
class FilterPanel(Panel):
    def __init__(self, parent, r_min_var, r_max_var, g_min_var, g_max_var, b_min_var, b_max_var):
        super().__init__(parent=parent)
        self.pack(fill='x', pady=4)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')
        self.columnconfigure(2, weight=2, uniform='a')

        label = ctk.CTkLabel(self, text="Channel")
        label.grid(column=0, row=0, sticky='E')
        label = ctk.CTkLabel(self, text="Min")
        label.grid(column=1, row=0)
        label = ctk.CTkLabel(self, text="Max")
        label.grid(column=2, row=0)
        
        label = ctk.CTkLabel(self, text="R")
        label.grid(column=0, row=1, pady=5, sticky='E')
        r_entry = ctk.CTkEntry(self, width=50, textvariable=r_min_var)
        r_entry.grid(column=1, row=1, pady=5)
        r_entry = ctk.CTkEntry(self, width=50, textvariable=r_max_var)
        r_entry.grid(column=2, row=1, pady=5)

        label = ctk.CTkLabel(self, text="G")
        label.grid(column=0, row=2, pady=5, sticky='E')
        g_entry = ctk.CTkEntry(self, width=50, textvariable=g_min_var)
        g_entry.grid(column=1, row=2, pady=5)
        g_entry = ctk.CTkEntry(self, width=50, textvariable=g_max_var)
        g_entry.grid(column=2, row=2, pady=5)

        label = ctk.CTkLabel(self, text="B")
        label.grid(column=0, row=3, pady=5, sticky='E')
        b_entry = ctk.CTkEntry(self, width=50, textvariable=b_min_var)
        b_entry.grid(column=1, row=3, pady=5)
        b_entry = ctk.CTkEntry(self, width=50, textvariable=b_max_var)
        b_entry.grid(column=2, row=3, pady=5)


# Edit Frame
class ChannelPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_var, options):
        super().__init__(master=parent, values=options, fg_color='#4a4a4a',
                         button_color='#444', button_hover_color='#333', dropdown_fg_color='#666', variable=data_var, command=self.updateChannel)
        self.pack(fill='x', pady=4)

    def updateChannel(self, parent):
        self._variable.set(parent)


class EditPanel(Panel):
    def __init__(self, parent, r_var, g_var, b_var, a_var, manipulate_image):
        super().__init__(parent=parent)
        self.pack(fill='x', pady=4)

        self.r_var = r_var
        self.g_var = g_var
        self.b_var = b_var

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=3, uniform='a')

        rgb_register = self.register(self.validate_rgb)

        # Hex Entry
        label = ctk.CTkLabel(self, text="HEX")
        label.grid(column=0, row=0, pady=5, sticky='E')
        hex_entry = ctk.CTkEntry(self)
        hex_entry.grid(column=1, row=0, pady=5)

        # Convert Hex to RGB button
        convert_button = ctk.CTkButton(self, text="Convert to RGB", command=lambda: self.hex_to_rgb(self.hex_entry.get()))
        convert_button.grid(column=0, row=1, columnspan=2, pady=(0, 30))

        # R value
        label = ctk.CTkLabel(self, text="R")
        label.grid(column=0, row=2, pady=5, sticky='E')
        r_entry = ctk.CTkEntry(self,  textvariable=r_var, validate="key", validatecommand=(rgb_register, '%P'))
        r_entry.grid(column=1, row=2, pady=5)
        r_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=r_var)
        r_slider.grid(column=0, row=3, columnspan=2, pady=(0, 10))

        # G value
        label = ctk.CTkLabel(self, text="G")
        label.grid(column=0, row=4, pady=5, sticky='E')
        g_entry = ctk.CTkEntry(self, textvariable=g_var, validate="key", validatecommand=(rgb_register, '%P'))
        g_entry.grid(column=1, row=4, pady=5)
        g_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=g_var)
        g_slider.grid(column=0, row=5, columnspan=2, pady=(0, 10))

        # B value
        label = ctk.CTkLabel(self, text="B")
        label.grid(column=0, row=6, pady=5, sticky='E')
        b_entry = ctk.CTkEntry(self, textvariable=b_var, validate="key", validatecommand=(rgb_register, '%P'))
        b_entry.grid(column=1, row=6, pady=5)
        b_slider = ctk.CTkSlider(self, from_=RGB_MIN, to=RGB_MAX, width=200, variable=b_var)
        b_slider.grid(column=0, row=7, columnspan=2, pady=(0, 10))

        # A value
        label = ctk.CTkLabel(self, text="A")
        label.grid(column=0, row=8, pady=5, sticky='E')
        a_entry = ctk.CTkEntry(self, textvariable=a_var)
        a_entry.grid(column=1, row=8, pady=5)
        a_slider = ctk.CTkSlider(self, from_=ALPHA_MIN, to=ALPHA_MAX, width=200, variable=a_var)
        a_slider.grid(column=0, row=9, columnspan=2, pady=(0, 10))

        # View Changes button
        apply_button = ctk.CTkButton(self, text="View Changes", command=manipulate_image)
        apply_button.grid(column=0, row=10, columnspan=2, pady=(0, 10))

    def hex_to_rgb(self, hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)

        self.r_var.set(rgb[0])
        self.g_var.set(rgb[1])
        self.b_var.set(rgb[2])
    
    def validate_rgb(self, num):
        if num:
            if num.isdigit() and int(num) in range(0, 256):
                return True
            else:
                return False
        else:
            return True


# Export Frame
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

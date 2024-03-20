import customtkinter as ctk
from canvas import *
from panels import *
from settings import *


class Menu(ctk.CTkTabview):
    def __init__(self, parent,
                 r_min_var, r_max_var, g_min_var, g_max_var, b_min_var, b_max_var, # current filters
                 r_var, g_var, b_var, a_var, # current rgba
                 channels_var, # current channel
                 manipulate_image, import_image='', export_image='' # functions
    ):
                  
        super().__init__(master=parent)
        self.grid(column=0, row=0, sticky='nsew', padx=10, pady=10)

        # create tabs
        self.add("Import")
        self.add("Filter")
        self.add("Edit")
        self.add("Export")

        # Widgets
        ImportFrame(self.tab('Import'), import_image)
        FilterFrame(self.tab('Filter'), r_min_var, r_max_var, g_min_var, g_max_var, b_min_var, b_max_var)
        EditFrame(self.tab('Edit'), channels_var, r_var, g_var, b_var, a_var, manipulate_image)
        ExportFrame(self.tab('Export'), export_image)


class ImportFrame(ctk.CTkFrame):
    def __init__(self, parent, import_image):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        OpenButton(self, import_image)


class FilterFrame(ctk.CTkFrame):
    def __init__(self, parent, r_min_var, r_max_var, g_min_var, g_max_var, b_min_var, b_max_var):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        FilterPanel(self, r_min_var, r_max_var, g_min_var, g_max_var, b_min_var, b_max_var)
       

class EditFrame(ctk.CTkFrame):
    def __init__(self, parent, channels_var, r_var, g_var, b_var, a_var, manipulate_image):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        DropdownPanel(self, channels_var, CHANNELS)
        ColorPanel(self, r_var, g_var, b_var, a_var, manipulate_image)
        

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent, export_image):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar(value='png')
        self.path_string = ctk.StringVar()

        FileNamePanel(self, self.name_string, self.file_string)
        FilePathPanel(self, self.path_string)
        SaveButton(self, export_image, self.name_string,
                   self.file_string, self.path_string)

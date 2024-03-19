import customtkinter as ctk
from tkinter import StringVar, IntVar, DoubleVar  # Add DoubleVar
from PIL import Image, ImageTk
from canvas import *
from menu import Menu
from settings import *

# Global variables
image = None
modified_image = None


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Color Substitution')
        self.minsize(800, 500)
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # canvas
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        self.menu = Menu(self, self.channels_var, self.alpha_var, self.r_var, self.g_var, self.b_var, import_image=self.import_image)
        # print(self.alpha_var.get())
        
        # run
        self.mainloop()

    def init_parameters(self):
        self.r_var = IntVar(value=0)
        self.g_var = IntVar(value=0)
        self.b_var = IntVar(value=0)
        self.alpha_var = DoubleVar(value=1.0)

        self.channels_var = StringVar(value = CHANNELS[0])

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_output = ImageOutput(self, self.resize_image)
        self.menu = Menu(self, self.channels_var, self.alpha_var, self.r_var, self.g_var, self.b_var, import_image=self.import_image, export_image=self.export_image, manipulate_image=self.original)

    # def manipulate_image(self, *args):
    #     self.image = self.original

    #     self.image

    #     self.place_image()

    def resize_image(self, event):

        # get canvas ratio
        canvas_ratio = event.width / event.height

        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # resize image
        if canvas_ratio > self.image_ratio:  # canvas wider than image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:  # canvas taller than image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        
        self.place_image()
    
    def place_image(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(
            self.canvas_width/2, self.canvas_height/2, image=self.image_tk)

    
    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)
        



app = App()

# OLD CODE BELOW HERE

# def identify_channels():
#     if image:
#         if image.mode == "RGBA":
#             return True
#         elif image.mode == "RGB":
#             return False

# def apply_color():
#     global image, modified_image

#     def within_range(pixel, r_range, g_range, b_range):
#         r, g, b, _ = pixel
#         return r_range[0] <= r <= r_range[1] and g_range[0] <= g <= g_range[1] and b_range[0] <= b <= b_range[1]

#     if image:
#         r_min_val, r_max_val = r_min.get(), r_max.get()
#         g_min_val, g_max_val = g_min.get(), g_max.get()
#         b_min_val, b_max_val = b_min.get(), b_max.get()
#         a_val = add_alpha_var.get()  # Value of channel A

#         # Function to convert a pixel to a new pixel
#         def convert_pixel(pixel):
#             nonlocal r_min_val, r_max_val, g_min_val, g_max_val, b_min_val, b_max_val, a_val
#             if within_range(pixel, (r_min_val, r_max_val), (g_min_val, g_max_val), (b_min_val, b_max_val)):
#                 # Add the specified values to the R, G, B, and A channels
#                 r, g, b, a = pixel
#                 r += add_r_var.get()
#                 g += add_g_var.get()
#                 b += add_b_var.get()
#                 a += a_val

#                 # Limit the values to be in the range of 0 to 255 and 0.0 to 1.0
#                 r = max(0, min(255, int(r)))
#                 g = max(0, min(255, int(g)))
#                 b = max(0, min(255, int(b)))
#                 # Scale float alpha to integer range (0-255)
#                 a = max(0, min(255, int(a * 255)))

#                 # Check the choice of channel order
#                 if order_var.get() == "RGBA":
#                     return (r, g, b, a)
#                 elif order_var.get() == "RBGA":
#                     return (r, b, g, a)
#                 elif order_var.get() == "BGRA":
#                     return (b, g, r, a)
#                 elif order_var.get() == "BRGA":
#                     return (b, r, g, a)
#                 elif order_var.get() == "GRBA":
#                     return (g, r, b, a)
#                 elif order_var.get() == "GBRA":
#                     return (g, b, r, a)
#             return pixel

#         # Apply color substitution to the image
#         modified_image = image.convert(
#             "RGBA" if identify_channels() else "RGB")
#         modified_image.putdata(list(map(convert_pixel, image.getdata())))

#         # Display the modified image
#         image_tk = ImageTk.PhotoImage(modified_image)
#         image_label.configure(image=image_tk)
#         image_label.image = image_tk

# def create_range_frame():
#     range_frame = ctk.CTkFrame(root)
#     range_frame.pack()

#     # Configuration for the R channel (red)
#     r_label = ctk.CTkLabel(range_frame, text="R Channel:")
#     r_label.pack(side=ctk.LEFT)

#     r_min_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Min")
#     r_min_scale.pack(side=ctk.LEFT)

#     r_max_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Max")
#     r_max_scale.pack(side=ctk.LEFT)

#     # Configuration for the G channel (green)
#     g_label = ctk.CTkLabel(range_frame, text="G Channel:")
#     g_label.pack(side=ctk.LEFT)

#     g_min_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Min")
#     g_min_scale.pack(side=ctk.LEFT)

#     g_max_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Max")
#     g_max_scale.pack(side=ctk.LEFT)

#     # Configuration for the B channel (blue)
#     b_label = ctk.CTkLabel(range_frame, text="B Channel:")
#     b_label.pack(side=ctk.LEFT)

#     b_min_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Min")
#     b_min_scale.pack(side=ctk.LEFT)

#     b_max_scale = Scale(range_frame, from_=0, to=255,
#                         orient=ctk.HORIZONTAL, length=200, label="Max")
#     b_max_scale.pack(side=ctk.LEFT)

#     return r_min_scale, r_max_scale, g_min_scale, g_max_scale, b_min_scale, b_max_scale

# # Create a frame for widgets
# frame = ctk.CTkFrame(root)
# frame.pack()

# # Create a button to apply color substitution
# apply_button = ctk.CTkButton(frame, text="Apply color", command=apply_color)
# apply_button.grid(row=3, column=0, padx=20, pady=20)

# # Create a range frame
# r_min, r_max, g_min, g_max, b_min, b_max = create_range_frame()

# # Create variables to store the choice of order and values to add
# order_var = StringVar(value="RGBA")
# add_r_var = IntVar(value=0)
# add_g_var = IntVar(value=0)
# add_b_var = IntVar(value=0)

# add_button = ctk.CTkButton(frame, text="Adjust RGB",
#                            command=open_add_values_window)
# add_button.grid(row=2, column=1, padx=20, pady=20)
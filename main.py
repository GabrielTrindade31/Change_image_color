import customtkinter as ctk
from tkinter import filedialog, Scale, Toplevel, StringVar, Radiobutton, IntVar, DoubleVar  # Add DoubleVar
from PIL import Image, ImageTk
from image_widgets import *
from menu import Menu

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

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        self.image_import = ImageImport(self, self.import_image)

        # self.menu = Menu(self)

        # run
        self.mainloop()

    def import_image(self, path):
        global image
        self.image = Image.open(path)
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        self.menu = Menu(self)

    def resize_image(self, event):

        canvas_ratio = event.width / event.height

        # reize image
        if canvas_ratio > self.image_ratio:  # canvas wider than image
            image_height = int(event.height)
            image_width = int(image_height * self.image_ratio)
        else:  # canvas taller than image
            image_width = int(event.width)
            image_height = int(image_width / self.image_ratio)

        # place image
        self.image_output.delete('all')
        resized_image = self.image.resize((image_width, image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(
            event.width/2, event.height/2, image=self.image_tk)

        # self.tab_view = MyTabView(master=self)
        # self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()

# class MyTabView(ctk.CTkTabview):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)

#         # create tabs
#         self.add("Import")
#         self.add("Edit")
#         self.add("Export")

#         # Widgets
#         self.image_import = ImageImport(self.tab("Import"), self.import_image)

#         self.label = ctk.CTkLabel(master=self.tab("Edit"))
#         self.label.grid(row=0, column=0, padx=20, pady=10)

#     def import_image(self, path):
#         global image
#         self.image = Image.open(path)
#         self.image_ratio = self.image.size[0] / self.image.size[1]
#         self.image_tk = ImageTk.PhotoImage(self.image)

#         self.image_output = ImageOutput(self, self.resize_image)

#     def resize_image(self, event):

#         canvas_ratio = event.width / event.height

#         # reize image
#         if canvas_ratio > self.image_ratio:  # canvas wider than image
#             image_height = int(event.height)
#             image_width = int(image_height * self.image_ratio)
#         else:  # canvas taller than image
#             image_width = int(event.width)
#             image_height = int(image_width / self.image_ratio)

#         # place image
#         self.image_output.delete('all')
#         resized_image = self.image.resize((image_width, image_height))
#         self.image_tk = ImageTk.PhotoImage(resized_image)
#         self.image_output.create_image(
#             event.width/2, event.height/2, image=self.image_tk)


# OLD CODE BELOW HERE


# # Function to open the image file
# def open_file():
#     global image
#     path = filedialog.askopenfilename()
#     image = Image.open(path)

#     # Display the original image
#     image_tk = ImageTk.PhotoImage(image)
#     image_label.configure(image=image_tk)
#     image_label.image = image_tk

# # Function to apply color substitution
# # Function to identify if the image is RGB or RGBA


# def identify_channels():
#     if image:
#         if image.mode == "RGBA":
#             return True
#         elif image.mode == "RGB":
#             return False

# # Function to add values to channel A


# def open_add_alpha_window():
#     add_alpha_window = Toplevel(root)
#     add_alpha_window.title("Add Value to Channel A")

#     # Slider to add value to channel A
#     alpha_slider = Scale(add_alpha_window, from_=0.0, to=1.0, resolution=0.01,
#                          orient=ctk.HORIZONTAL, length=200, label="Add to Channel A")
#     alpha_slider.set(add_alpha_var.get())
#     alpha_slider.pack()

#     # Button to confirm and apply the value
#     confirm_alpha_button = ctk.Button(add_alpha_window, text="Confirm", command=lambda: save_and_add_alpha(
#         alpha_slider.get(), add_alpha_window))
#     confirm_alpha_button.pack()

# # Function to save and add value to channel A


# def save_and_add_alpha(add_alpha, window):
#     add_alpha_var.set(add_alpha)
#     window.destroy()
#     apply_color()  # Call the function to update the modified image after changing channel A

# # Create a variable to store the value to add to channel A


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

# # Function to create a range frame


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

# # Function to create the channel order change window


# def open_order_change_window():
#     order_change_window = Toplevel(root)
#     order_change_window.title("Change Channel Order")

#     options = ["RGBA", "RBGA", "BGRA", "BRGA", "GRBA", "GBRA"]

#     # Variable to store the selected option
#     choice_var = StringVar(value=order_var.get())

#     # Create option buttons for channel orders
#     for option in options:
#         option_button = Radiobutton(
#             order_change_window, text=option, variable=choice_var, value=option)
#         option_button.pack()

#     # Button to confirm the choice
#     confirm_button = ctk.CTkButton(order_change_window, text="Confirm", command=lambda: save_and_change_order(
#         choice_var.get(), order_change_window))
#     confirm_button.pack()

# # Function to save and change the channel order


# def save_and_change_order(order, window):
#     order_var.set(order)
#     window.destroy()

# # Function to create the add values to channels window


# def open_add_values_window():
#     add_values_window = Toplevel(root)
#     add_values_window.title("Add Values to Channels")

#     # Sliders to add values to R, G, B channels
#     slider_r = Scale(add_values_window, from_=-255, to=255,
#                      orient=ctk.HORIZONTAL, length=200, label="Add to R Channel")
#     slider_r.set(add_r_var.get())
#     slider_r.pack()

#     slider_g = Scale(add_values_window, from_=-255, to=255,
#                      orient=ctk.HORIZONTAL, length=200, label="Add to G Channel")
#     slider_g.set(add_g_var.get())
#     slider_g.pack()

#     slider_b = Scale(add_values_window, from_=-255, to=255,
#                      orient=ctk.HORIZONTAL, length=200, label="Add to B Channel")
#     slider_b.set(add_b_var.get())
#     slider_b.pack()

#     # Button to confirm and apply the values
#     confirm_button = ctk.Button(add_values_window, text="Confirm", command=lambda: save_and_add_values(
#         slider_r.get(), slider_g.get(), slider_b.get(), add_values_window))
#     confirm_button.pack()

# # Function to save and add values to R, G, B channels


# def save_and_add_values(add_r, add_g, add_b, window):
#     add_r_var.set(add_r)
#     add_g_var.set(add_g)
#     add_b_var.set(add_b)
#     window.destroy()

# # Function to save the modified image


# def save_image():
#     global modified_image
#     if modified_image:
#         path = filedialog.asksaveasfilename(
#             defaultextension=".png", filetypes=[("PNG Files", "*.png")])
#         if path:
#             modified_image.save(path)


# def validate(P):
#     if len(P) == 0:
#         # empty Entry is ok
#         return True
#     elif P.isdigit() and P >= 0 and P <= 255:
#         return True
#     else:
#         return False


# # Create the main window
# root = ctk.CTk()
# root.title("Color Substitution")

# # Create a frame for widgets
# frame = ctk.CTkFrame(root)
# frame.pack()

# # Create a button to open the image file
# open_file_button = ctk.CTkButton(frame, text="Open file", command=open_file)
# open_file_button.grid(row=0, column=0, padx=20, pady=20)

# # Create a label to display the modified image
# image_label = ctk.CTkLabel(root)
# image_label.pack()

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

# # Create "Change" and "Add" buttons
# change_button = ctk.CTkButton(frame, text="Change Channel Order",
#                               command=open_order_change_window)
# change_button.grid(row=2, column=0, padx=20, pady=20)

# add_button = ctk.CTkButton(frame, text="Adjust RGB",
#                            command=open_add_values_window)
# add_button.grid(row=2, column=1, padx=20, pady=20)

# add_alpha_var = DoubleVar(value=1.0)
# add_alpha_button = ctk.CTkButton(
#     frame, text="Adjust A", command=open_add_alpha_window)
# add_alpha_button.grid(row=2, column=2, padx=20, pady=20)


# # Button to save the image
# save_button = ctk.CTkButton(frame, text="Save Image", command=save_image)
# save_button.grid(row=3, column=1, padx=20, pady=20)

# # vcmd = (root.register(validate), '%P')

# # r_lower = ctk.CTkEntry(root, placeholder_text="0",
# #                        validate="key", validatecommand=vcmd)
# # r_lower.pack()

# # r_upper = ctk.CTkEntry(root, placeholder_text="255",
# #                        validate="key", validatecommand=vcmd)
# # r_upper.pack()


# # Start the main loop
# root.mainloop()
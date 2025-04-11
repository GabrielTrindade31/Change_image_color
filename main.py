import customtkinter as ctk
import threading
import queue
import numpy as np
from customtkinter import StringVar, IntVar, DoubleVar
from PIL import Image, ImageTk
from canvas import *
from menu import Menu
from settings import *

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

        # processing queue
        self.process_queue = queue.Queue()
        self.after(100, self._process_queue)

        self.menu = Menu(self,
                         self.r_min_var, self.r_max_var, self.g_min_var, self.g_max_var, self.b_min_var, self.b_max_var,  # current filters
                         self.r_var, self.g_var, self.b_var, self.a_var,  # current rgba
                         self.channels_var,  # current channel
                         self.manipulate_image, import_image=self.import_image  # functions
                         )

        # run
        self.mainloop()

    def init_parameters(self):
        # current filter
        self.r_min_var = IntVar(value=0)
        self.r_max_var = IntVar(value=0)
        self.g_min_var = IntVar(value=0)
        self.g_max_var = IntVar(value=0)
        self.b_min_var = IntVar(value=0)
        self.b_max_var = IntVar(value=0)

        # current rgba
        self.r_var = IntVar(value=0)
        self.g_var = IntVar(value=0)
        self.b_var = IntVar(value=0)
        self.a_var = DoubleVar(value=0.0)

        # current channel
        self.channels_var = StringVar(value=CHANNELS[0])

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_output = ImageOutput(self, self.resize_image)
        Menu(self,
             self.r_min_var, self.r_max_var, self.g_min_var, self.g_max_var, self.b_min_var, self.b_max_var,  # current filters
             self.r_var, self.g_var, self.b_var, self.a_var,  # current rgba
             self.channels_var,  # current channel
             self.manipulate_image, import_image=self.import_image, export_image=self.export_image  # functions
             )

    def manipulate_image(self):
        # Add to processing queue instead of direct execution
        self.process_queue.put(self._process_image_task)
        self._show_processing(True)

    def _process_queue(self):
        try:
            while True:
                task = self.process_queue.get_nowait()
                # Create a thread for each task
                processing_thread = threading.Thread(
                    target=task,
                    daemon=True
                )
                processing_thread.start()
        except queue.Empty:
            pass
        self.after(100, self._process_queue)

    def _process_image_task(self):
        try:
            # Process the image in background
            processed_image = self._process_image_data()
            
            # Update UI on main thread
            self.after(0, self._update_image, processed_image)
            
        except Exception as e:
            self.after(0, self._show_error, str(e))
        finally:
            # Hide processing indicator
            self.after(0, self._show_processing, False)

    def _process_image_data(self):
        image = self.original.copy()
        img_array = np.array(image)
        
        # Get filter ranges
        r_min, r_max = self.r_min_var.get(), self.r_max_var.get()
        g_min, g_max = self.g_min_var.get(), self.g_max_var.get()
        b_min, b_max = self.b_min_var.get(), self.b_max_var.get()
        
        # Get replacement values
        new_r = np.clip(self.r_var.get(), 0, 255)
        new_g = np.clip(self.g_var.get(), 0, 255)
        new_b = np.clip(self.b_var.get(), 0, 255)
        new_a = np.clip(int(self.a_var.get() * 255), 0, 255)
        
        # Create mask for pixels within range
        if img_array.ndim == 3:  # RGB image
            r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
            mask = (
                (r >= r_min) & (r <= r_max) &
                (g >= g_min) & (g <= g_max) &
                (b >= b_min) & (b <= b_max)
            )
            
            # Only process pixels that match the mask
            if np.any(mask):
                # Create new pixel values
                channel_order = self.channels_var.get()
                if channel_order == "RGBA":
                    new_pixels = [new_r, new_g, new_b]
                elif channel_order == "RBGA":
                    new_pixels = [new_r, new_b, new_g]
                elif channel_order == "BGRA":
                    new_pixels = [new_b, new_g, new_r]
                elif channel_order == "BRGA":
                    new_pixels = [new_b, new_r, new_g]
                elif channel_order == "GRBA":
                    new_pixels = [new_g, new_r, new_b]
                elif channel_order == "GBRA":
                    new_pixels = [new_g, new_b, new_r]
                
                # Apply changes only to masked pixels
                for i in range(3):
                    img_array[:,:,i][mask] = new_pixels[i]
        
        elif img_array.ndim == 4:  # RGBA image
            r, g, b, a = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]
            mask = (
                (r >= r_min) & (r <= r_max) &
                (g >= g_min) & (g <= g_max) &
                (b >= b_min) & (b <= b_max)
            )
            
            # Only process pixels that match the mask
            if np.any(mask):
                channel_order = self.channels_var.get()
                if channel_order == "RGBA":
                    img_array[:,:,0][mask] = new_r
                    img_array[:,:,1][mask] = new_g
                    img_array[:,:,2][mask] = new_b
                elif channel_order == "RBGA":
                    img_array[:,:,0][mask] = new_r
                    img_array[:,:,1][mask] = new_b
                    img_array[:,:,2][mask] = new_g
                elif channel_order == "BGRA":
                    img_array[:,:,0][mask] = new_b
                    img_array[:,:,1][mask] = new_g
                    img_array[:,:,2][mask] = new_r
                elif channel_order == "BRGA":
                    img_array[:,:,0][mask] = new_b
                    img_array[:,:,1][mask] = new_r
                    img_array[:,:,2][mask] = new_g
                elif channel_order == "GRBA":
                    img_array[:,:,0][mask] = new_g
                    img_array[:,:,1][mask] = new_r
                    img_array[:,:,2][mask] = new_b
                elif channel_order == "GBRA":
                    img_array[:,:,0][mask] = new_g
                    img_array[:,:,1][mask] = new_b
                    img_array[:,:,2][mask] = new_r
                
                # Handle alpha channel separately
                img_array[:,:,3][mask] = np.clip(a[mask] + new_a, 0, 255)
    
        return Image.fromarray(img_array)

    def _update_image(self, processed_image):
        self.image = processed_image
        self.place_image()

    def _show_error(self, message):
        if hasattr(self, 'menu') and hasattr(self.menu, 'export_frame'):
            self.menu.export_frame.update_status(False, message)

    def _show_processing(self, show):
        if show:
            if not hasattr(self, 'progress_frame'):
                self.progress_frame = ctk.CTkFrame(self, corner_radius=10)
                self.progress_frame.place(relx=0.5, rely=0.5, anchor='center')
                
                self.progress_label = ctk.CTkLabel(
                    self.progress_frame, 
                    text="Processing image...", 
                    text_color="white"
                )
                self.progress_label.pack(pady=5, padx=10)
                
                self.progress_bar = ctk.CTkProgressBar(
                    self.progress_frame, 
                    width=200,
                    mode='indeterminate'
                )
                self.progress_bar.pack(pady=(0, 10), padx=10)
                self.progress_bar.start()
        elif hasattr(self, 'progress_frame'):
            self.progress_frame.destroy()
            del self.progress_frame
            del self.progress_label
            del self.progress_bar

    def resize_image(self, event):
        canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height

        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def place_image(self):
        self.image_output.delete('all')
        if hasattr(self, 'image'):
            resized_image = self.image.resize((self.image_width, self.image_height))
            self.image_tk = ImageTk.PhotoImage(resized_image)
            self.image_output.create_image(
                self.canvas_width/2, self.canvas_height/2, 
                image=self.image_tk
            )

    def export_image(self, name, file, path):
        try:
            if not name:
                raise ValueError("File name cannot be empty")
            if not path:
                raise ValueError("Path cannot be empty")
                
            export_string = f'{path}/{name}.{file}'
            self.image.save(export_string)
            return True
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")


app = App()
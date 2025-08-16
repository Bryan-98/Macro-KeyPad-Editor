import customtkinter as ctk
from PIL import Image

class ActivityLight(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.connected_path = "./assets/images/connect.png"
        self.disconnected_path = "./assets/images/disconnect.png"
        self.light_status = False

        self.light = None
        self.label = None

        self.create_widget()

    def create_widget(self):
        
        activity = ctk.CTkImage(dark_image=Image.open(self.disconnected_path),size=(20, 20))

        self.light = ctk.CTkLabel(self, text="", image=activity)
        self.light.grid(row=0, column=0, padx=10, pady=10)

        self.label = ctk.CTkLabel(self, text="Disconnected")
        self.label.grid(row=0, column=1, padx=10, pady=10)

    def set_activity_status(self, connection):
        if connection:
            activity = ctk.CTkImage(dark_image=Image.open(self.connected_path),size=(20, 20))
            self.label.configure(text="Connected")
            self.light_status = True
        else:
            activity = ctk.CTkImage(dark_image=Image.open(self.disconnected_path),size=(20, 20))
            self.label.configure(text="Disconnected")
            self.light_status = False
            
        self.light.configure(image=activity)
    
    def get_activity_status(self):
        return self.light_status


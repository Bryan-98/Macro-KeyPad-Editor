import customtkinter as ctk
from PIL import Image

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        # Main window setup
        super().__init__(parent)
        width = 780
        height = 430
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        
        x = (s_width / 2) - (width/2)
        y = (s_height / 2) - (height/2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color='green')
        self.overrideredirect(True)
        self.wm_attributes("-disabled", True)
        self.wm_attributes("-transparentcolor", 'green')

        self.create_widget()

    def create_widget(self):
        splash = ctk.CTkImage(dark_image=Image.open("./assets/images/splash.png"),size=(800, 450))
        ctk.CTkLabel(self, text="", image=splash).pack()

def start_splash_win(self):
    # Start the splash window and close after 3 seconds
    if self.splah_win  is None or not self.splah_win.winfo_exists():
        self.splah_win = SplashScreen(self)
        self.splah_win.after(3000, lambda:self.splah_win.destroy())
    else:
        self.splah_win.focus()

    # Wait for window to close
    self.wait_window(self.splah_win)
import serial.tools.list_ports
import customtkinter as ctk
from tkinter import Menu, Toplevel, Button, StringVar, OptionMenu
from encoder_frame import EncoderFrame
from key_button_frame import KeyButtonFrame
from led_frame import LedFrame

class App(ctk.CTk):

    def __init__(self, title, size):

        # Main window setup
        super().__init__()
        self.title(title)

        # self.geometry(f'{size[0]}x{size[1]}')
        self.center_window(size)
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Run Widgets
        self.create_widget()

        #run menu
        self.create_menu()

        # Run App
        self.mainloop()

    def create_widget(self):
        
        #Key buttons widget
        key_button_widget = KeyButtonFrame(self,arduino)
        key_button_widget.grid(row=0, column=0, padx=50, pady=50)
        
        #Encoder widget
        encoder_widget = EncoderFrame(self,arduino)
        encoder_widget.grid(row=0, column=1, padx=50, pady=50)
        
        #Led picker widget
        led_frame = LedFrame(self,arduino)
        led_frame.grid(row=0, column=2, padx=50, pady=50)

    def create_menu(self):
        def donothing():
            filewin = Toplevel(self)
            button = Button(filewin, text="Do nothing button")
            button.pack()

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=donothing)
        editmenu.add_command(label="Copy", command=donothing)
        editmenu.add_command(label="Paste", command=donothing)
        editmenu.add_command(label="Delete", command=donothing)
        editmenu.add_command(label="Select All", command=donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=donothing)
        helpmenu.add_command(label="About...", command=donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)

    def center_window(self, size):
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        
        x = (s_width / 2) - (size[0]/2)
        y = (s_height / 2) - (size[1]/2)

        self.geometry('%dx%d+%d+%d' % (size[0], size[1], x, y))


if __name__ == "__main__":
    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0.1)
    App('KeyPad Editor', (1080,608))
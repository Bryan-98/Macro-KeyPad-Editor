import serial
import customtkinter as ctk
import tkinter as tk
from tkinter import StringVar, IntVar
from controller.arduino_connection import send_rgb_values
from controller.create_save_folder import last_saved_led

class LedFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        #Setting variables
        self.arduino = None
        self.apply_btn = None
        self.red_var = IntVar(self)
        self.green_var = IntVar(self)
        self.blue_var = IntVar(self)
        self.led = None
        self.slider_red = None
        self.slider_green = None
        self.slider_blue = None
        self.error_msg = StringVar(self)

        #Creating led widgets
        self.create_widgets()

    def create_widgets(self):
        
        #Canvas to disaply current window
        self.led = tk.Canvas(self, bg="blue", height=50, width=50)
        self.led.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        #Setting default vaules for led windo and widgets
        self.red_var.set(0)
        self.green_var.set(251)
        self.blue_var.set(255)
        self.led.configure(bg=(f'#{int(self.red_var.get()):02x}{int(self.green_var.get()):02x}{int(self.blue_var.get()):02x}'))

        #Change the led window and sliders to user selected values
        def change_canvas(value):
            self.led.configure(bg=(f'#{int(self.red_var.get()):02x}{int(self.green_var.get()):02x}{int(self.blue_var.get()):02x}'))
            red_entry.configure(textvariable=StringVar(self, value=self.red_var.get()))
            green_entry.configure(textvariable=StringVar(self, value=self.green_var.get()))
            blue_entry.configure(textvariable=StringVar(self, value=self.blue_var.get()))

        #setting the color of the slider
        red_color = (f'#{242:02x}{84:02x}{73:02x}')
        green_color = (f'#{55:02x}{179:02x}{55:02x}')
        blue_color = (f'#{56:02x}{64:02x}{181:02x}')

        #Creating the slider and entery to the Red slider
        self.slider_red = ctk.CTkSlider(self, from_=0, to=255, variable=self.red_var, orientation='vertical')
        self.slider_red.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=red_color, command=change_canvas, state="disabled")
        self.slider_red.grid(row=1, column=0, padx=10, pady=10)

        red_entry = ctk.CTkEntry(self, textvariable=StringVar(self, value=self.red_var.get()))
        red_entry.configure(width=40, height=30, state="disabled")
        red_entry.grid(row=2, column=0, padx=10, pady=10)

        #Creating the slider and entery to the Green slider
        self.slider_green = ctk.CTkSlider(self, from_=0, to=255, variable=self.green_var, orientation='vertical')
        self.slider_green.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=green_color, command=change_canvas, state="disabled")
        self.slider_green.grid(row=1, column=1, padx=10, pady=10)

        green_entry = ctk.CTkEntry(self, textvariable=StringVar(self, value=self.green_var.get()))
        green_entry.configure(width=40, height=30, state="disabled")
        green_entry.grid(row=2, column=1, padx=10, pady=10)

        #Creating the slider and entery to the blue slider
        self.slider_blue = ctk.CTkSlider(self, from_=0, to=255, variable=self.blue_var, orientation='vertical')
        self.slider_blue.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=blue_color, command=change_canvas, state="disabled")
        self.slider_blue.grid(row=1, column=2, padx=10, pady=10)

        blue_entry = ctk.CTkEntry(self, textvariable=StringVar(self, value=self.blue_var.get()))
        blue_entry.configure(width=40, height=30, state="disabled")
        blue_entry.grid(row=2, column=2, padx=10, pady=10)

        #Apply button send values to arduino
        self.apply_btn = ctk.CTkButton(self, text="Apply", command=self.save_rgb)
        self.apply_btn.configure(fg_color="white", text_color="black", hover_color=("black", "lightgray"), state="disabled")
        self.apply_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    #Send rgb values to arduino
    def save_rgb(self):
        try:
            rgb = f'{self.red_var.get()},{self.green_var.get()},{self.blue_var.get()}'
            send_rgb_values(self.arduino, rgb)
            
        except(serial.SerialException) as e:
                self.slider_red.configure(state="disabled")
                self.slider_green.configure(state="disabled")
                self.slider_blue.configure(state="disabled")
                self.apply_btn.configure(state="disabled")

    #Get current RGB values
    def get_rgb(self):
        values = [str(self.red_var.get()), str(self.green_var.get()), str(self.blue_var.get())]
        return values
    
    def set_arduino_connection(self, arduino):
        self.arduino = arduino
        self.apply_btn.configure(state="normal")
        self.slider_red.configure(state="normal")
        self.slider_green.configure(state="normal")
        self.slider_blue.configure(state="normal")
        self.save_rgb()
    
    def get_arduino_status(self):
        return self.error_msg.get()
    
    def init_set_rgb(self, red, green, blue):
        self.red_var.set(red)
        self.green_var.set(green)
        self.blue_var.set(blue)
        self.led.configure(bg=(f'#{int(self.red_var.get()):02x}{int(self.green_var.get()):02x}{int(self.blue_var.get()):02x}'))
        self.slider_red.configure(variable=self.red_var)
        self.slider_green.configure(variable=self.green_var)
        self.slider_blue.configure(variable=self.blue_var)
    
    #Set RGB vales for when restoing using profile
    def set_rgb(self, red, green, blue):
        self.red_var.set(red)
        self.green_var.set(green)
        self.blue_var.set(blue)
        self.led.configure(bg=(f'#{int(self.red_var.get()):02x}{int(self.green_var.get()):02x}{int(self.blue_var.get()):02x}'))
        self.slider_red.configure(variable=self.red_var)
        self.slider_green.configure(variable=self.green_var)
        self.slider_blue.configure(variable=self.blue_var)
        self.save_rgb()
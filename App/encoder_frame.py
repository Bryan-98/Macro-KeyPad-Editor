import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import StringVar
from backend import get_app_names, get_app_volume, set_app_volume

class EncoderFrame(ctk.CTkFrame):
    def __init__(self, container, arduino):
        super().__init__(container)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.arduino = arduino
        self.create_widget()
        
    def create_widget(self):
        # App selection
        options = get_app_names()

        # #Encoder 1
        dropdown_variable1 = StringVar(self)
        encoder1_dropdown = ctk.CTkOptionMenu(self, variable=dropdown_variable1, values=options, command=lambda event: update_dropdown(1, event))
        encoder1_dropdown.grid(row=0, column=0, padx=10, pady=10)
        encoder1_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"),   fg_color="white", button_color="white", dynamic_resizing=False)
        dropdown_variable1.set('Master Volume')

        #Encoder 2
        dropdown_variable2 = StringVar(self)
        encoder2_dropdown = ctk.CTkOptionMenu(self, variable=dropdown_variable2, values=options, command=lambda event: update_dropdown(2, event))
        encoder2_dropdown.grid(row=1, column=0, padx=10, pady=10)
        encoder2_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"),   fg_color="white", button_color="white", dynamic_resizing=False)
        dropdown_variable2.set('Master Volume')

        #Encoder 3
        dropdown_variable3 = StringVar(self)
        encoder3_dropdown = ctk.CTkOptionMenu(self, variable=dropdown_variable3, values=options, command=lambda event: update_dropdown(3, event))
        encoder3_dropdown.grid(row=2, column=0, padx=10, pady=10)
        encoder3_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"),   fg_color="white", button_color="white", dynamic_resizing=False)
        dropdown_variable3.set('Master Volume')

        def arduino_handler():
   
            volume1 = get_app_volume(dropdown_variable1.get())
            volume2 = get_app_volume(dropdown_variable2.get())
            volume3 = get_app_volume(dropdown_variable3.get())
            prev_1 = 0
            prev_2 = 0
            prev_2 = 0
            while True:
                data = self.arduino.readline().strip()
                
                if data and len(data.decode()) > 1:
                    print(data)
                    start, end = data.decode().split(":")
                    encoder_number = int(start)
                    encoder_pos = int(end)
                    if encoder_pos != 0:
                        if encoder_number == 1 and volume1 != None:
                            if (volume1 + encoder_pos) < 101 and (volume1 + encoder_pos) > 0:
                                volume1 += encoder_pos
                                if volume1 <= 100 and volume1 >= 0:
                                    set_app_volume(dropdown_variable1.get(), volume1)
                        elif encoder_number == 2 and volume2 != None:
                            if (volume2 + encoder_pos) < 101 and (volume2 + encoder_pos) > 0:
                                volume2 += encoder_pos
                                if volume2 <= 100 and volume2 >= 0:
                                    set_app_volume(dropdown_variable2.get(), volume2)
                        elif encoder_number == 3 and volume3 != None:
                            if (volume3 + encoder_pos) < 101 and (volume3 + encoder_pos) > 0:
                                volume3 += encoder_pos
                                if volume3 <= 100 and volume3 >= 0:
                                    set_app_volume(dropdown_variable3.get(), volume3)
                    else:
                        if encoder_number == 1 and volume1 != None:
                            if volume1 > 0:
                                prev_1 = volume1
                                volume1 = 0
                                set_app_volume(dropdown_variable1.get(), volume1)
                            else:
                                volume1 = prev_1
                                set_app_volume(dropdown_variable1.get(), volume1)
                        elif encoder_number == 2 and volume2 != None:
                            if volume2 > 0:
                                prev_2 = volume2
                                volume2 = 0
                                set_app_volume(dropdown_variable2.get(), volume2)
                            else:
                                volume2 = prev_2
                                set_app_volume(dropdown_variable2.get(), volume2)
                        elif encoder_number == 3 and volume3 != None:
                            if volume3 > 0:
                                prev_3 = volume3
                                volume3 = 0
                                set_app_volume(dropdown_variable3.get(), volume3)
                            else:
                                volume3 = prev_3
                                set_app_volume(dropdown_variable3.get(), volume3)


        threading.Thread(target=arduino_handler, daemon=True).start()

        def update_dropdown(slider, event):

            if slider == 1:
                dropdown_variable1.set(event)
            elif slider == 2:
                dropdown_variable2.set(event)
            else:
                dropdown_variable3.set(event)
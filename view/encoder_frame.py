import serial, threading
import customtkinter as ctk
from controller.arduino_connection import set_encoder
from tkinter import StringVar, BooleanVar
from controller.audio_backend import get_app_names, get_app_volume, set_app_volume, get_app_status

class EncoderFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.encoder1_state = BooleanVar(self, False)
        self.encoder2_state = BooleanVar(self, False)
        self.encoder3_state = BooleanVar(self, False)

        self.encoder1_dropdown = None
        self.encoder2_dropdown = None
        self.encoder3_dropdown = None

        self.dropdown_variable1 = StringVar(self)
        self.dropdown_variable2 = StringVar(self)
        self.dropdown_variable3 = StringVar(self)

        self.switch1 = None
        self.switch2 = None
        self.switch3 = None

        self.switch_var1 = StringVar(self)
        self.switch_var2 = StringVar(self)
        self.switch_var3 = StringVar(self)

        self.arduino = None
        self.options = None
        self.arduino_connection = False
        self.is_thread_running = True

        self.create_widget()

    def create_widget(self):
        # App selection
        self.options = get_app_names()
        red_color = (f'#{242:02x}{84:02x}{73:02x}')
        green_color = (f'#{55:02x}{179:02x}{55:02x}')

        # #Encoder 1
        self.encoder1_dropdown = ctk.CTkOptionMenu(self, variable=self.dropdown_variable1, values=self.options, command=lambda event: update_dropdown(1, event))
        self.encoder1_dropdown.grid(row=0, column=0, padx=10, pady=10)
        self.encoder1_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"), fg_color="white", button_color="white", dynamic_resizing=False, state="disabled")
        self.dropdown_variable1.set('Master Volume')

        self.switch_var1.set(value="on")
        self.switch1 = ctk.CTkSwitch(self, command= lambda:self.switch_audio(1, self.encoder1_dropdown, self.switch_var1), variable=self.switch_var1, onvalue="on", offvalue="off")
        self.switch1.configure(progress_color=red_color, fg_color=green_color, text="AW UP / AW DN", state="disabled")
        self.switch1.grid(row=0, column=1, padx=10, pady=10, sticky= 'w')

        #Encoder 2
        self.encoder2_dropdown = ctk.CTkOptionMenu(self, variable=self.dropdown_variable2, values=self.options, command=lambda event: update_dropdown(2, event))
        self.encoder2_dropdown.grid(row=1, column=0, padx=10, pady=10)
        self.encoder2_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"), fg_color="white", button_color="white", dynamic_resizing=False, state="disabled")
        self.dropdown_variable2.set('Master Volume')

        self.switch_var2.set(value="on")
        self.switch2 = ctk.CTkSwitch(self, command= lambda:self.switch_audio(2, self.encoder2_dropdown, self.switch_var2), variable=self.switch_var2, onvalue="on", offvalue="off")
        self.switch2.configure(progress_color=red_color, fg_color=green_color, text="AW LT / AW RT", state="disabled")
        self.switch2.grid(row=1, column=1, padx=10, pady=10, sticky= 'w')

        #Encoder 3
        self.encoder3_dropdown = ctk.CTkOptionMenu(self, variable=self.dropdown_variable3, values=self.options, command=lambda event: update_dropdown(3, event))
        self.encoder3_dropdown.grid(row=2, column=0, padx=10, pady=10)
        self.encoder3_dropdown.configure(text_color="black", button_hover_color=("black", "lightgray"), fg_color="white", button_color="white", dynamic_resizing=False, state="disabled")
        self.dropdown_variable3.set('Master Volume')

        self.switch_var3.set(value="on")
        self.switch3 = ctk.CTkSwitch(self, command= lambda:self.switch_audio(3, self.encoder3_dropdown, self.switch_var3), variable=self.switch_var3, onvalue="on", offvalue="off")
        self.switch3.configure(progress_color=red_color, fg_color=green_color, text="PG UP / PG DN", state="disabled")
        self.switch3.grid(row=2, column=1, padx=10, pady=10, sticky= 'w')

        def update_dropdown(slider, event):

            if slider == 1:
                self.dropdown_variable1.set(event)
            elif slider == 2:
                self.dropdown_variable2.set(event)
            else:
                self.dropdown_variable3.set(event)

    #Send rgb values to arduino
    def send_encoder(self, switchNum, value):

        buttonState = 0
        if(value.get() == "on"):
            buttonState = 1

        try:
            set_encoder(self.arduino, switchNum, buttonState)
            
        except(serial.SerialException, OSError) as e:
            print("Encoder has Stopped cannot send")

    def set_arduino_connection(self, arduino):
        self.arduino = arduino
        self.switch1.configure(state="normal")
        self.switch2.configure(state="normal")
        self.switch3.configure(state="normal")
        self.is_thread_running = True
        self.arduino_connection = True
        self.audio_controller_thread()

    def stop_encoder_thread(self):
        self.is_thread_running = False

    def check_arduino_connection(self):
        return self.arduino_connection

    def set_switches_off(self):
        self.switch_var1.set(value="on")
        self.switch1.configure(variable=self.switch_var1)
        self.switch_var2.set(value="on")
        self.switch2.configure(variable=self.switch_var2)
        self.switch_var3.set(value="on")
        self.switch3.configure(variable=self.switch_var3)

        self.encoder1_dropdown.configure(state="disabled")
        self.encoder2_dropdown.configure(state="disabled")
        self.encoder3_dropdown.configure(state="disabled")

        self.switch1.configure(state="disabled")
        self.switch2.configure(state="disabled")
        self.switch3.configure(state="disabled")

        self.encoder1_state.set(False)
        self.encoder2_state.set(False)
        self.encoder3_state.set(False)
        
    def switch_audio(self, switchNum, dropdown, value):
            if(value.get() == "on"):
                dropdown.configure(state="disabled")
                if switchNum == 1:
                    self.encoder1_state.set(False)
                elif switchNum == 2:
                    self.encoder2_state.set(False)
                else:
                    self.encoder3_state.set(False)
            else:
                dropdown.configure(state="normal")
                if switchNum == 1:
                    self.encoder1_state.set(True)
                elif switchNum == 2:
                    self.encoder2_state.set(True)
                else:
                    self.encoder3_state.set(True)

            if self.encoder1_state.get() == False and self.encoder2_state.get() == False and self.encoder3_state.get() == False:
                self.is_thread_running = False
            elif self.encoder1_state.get() == True or self.encoder2_state.get() == True or self.encoder3_state.get() == True:
                self.is_thread_running = True

            if not self.is_thread_running:
                self.audio_controller_thread()

            self.send_encoder(switchNum, value)

    def audio_controller_thread(self):

        def check_audio_options():
            new_options = get_app_names()
            if len(self.options) != len(new_options):
                self.options = new_options
                self.encoder1_dropdown.configure(values=self.options)
                self.encoder2_dropdown.configure(values=self.options)
                self.encoder3_dropdown.configure(values=self.options)
        
        def check_audio_disconnect(appName, encoder):
            if not get_app_status(appName):
                encoder.set(self.options[0])


        def arduino_handler():
            
            try:
                volume1 = get_app_volume(self.dropdown_variable1.get())
                volume2 = get_app_volume(self.dropdown_variable2.get())
                volume3 = get_app_volume(self.dropdown_variable3.get())
                prev_1 = 0
                prev_2 = 0
                prev_2 = 0
                while self.is_thread_running:
                    check_audio_options()
                    check_audio_disconnect(self.dropdown_variable1.get(), self.encoder1_dropdown)
                    check_audio_disconnect(self.dropdown_variable2.get(), self.encoder2_dropdown)
                    check_audio_disconnect(self.dropdown_variable3.get(), self.encoder3_dropdown)

                    data = self.arduino.readline().strip()
                    data = data.decode()
                    if data and len(data) > 1:
                        if data[0].isnumeric():
                            start, end = data.split(":")
                            encoder_number = int(start)
                            encoder_pos = int(end) 
                            if encoder_pos != 0:
                                if encoder_number == 1 and volume1 != None and self.encoder1_state.get() == True:
                                    if (volume1 + encoder_pos) < 101 and (volume1 + encoder_pos) > 0:
                                        volume1 += encoder_pos
                                        if volume1 <= 100 and volume1 >= 0:
                                            set_app_volume(self.dropdown_variable1.get(), volume1)
                                elif encoder_number == 2 and volume2 != None and self.encoder2_state.get() == True:
                                    if (volume2 + encoder_pos) < 101 and (volume2 + encoder_pos) > 0:
                                        volume2 += encoder_pos
                                        if volume2 <= 100 and volume2 >= 0:
                                            set_app_volume(self.dropdown_variable2.get(), volume2)
                                elif encoder_number == 3 and volume3 != None and self.encoder3_state.get() == True:
                                    if (volume3 + encoder_pos) < 101 and (volume3 + encoder_pos) > 0:
                                        volume3 += encoder_pos
                                        if volume3 <= 100 and volume3 >= 0:
                                            set_app_volume(self.dropdown_variable3.get(), volume3)
                            else:
                                if encoder_number == 1 and volume1 != None and self.encoder1_state.get() == True:
                                    if volume1 > 0:
                                        prev_1 = volume1
                                        volume1 = 0
                                        set_app_volume(self.dropdown_variable1.get(), volume1)
                                    else:
                                        volume1 = prev_1
                                        set_app_volume(self.dropdown_variable1.get(), volume1)
                                elif encoder_number == 2 and volume2 != None and self.encoder2_state.get() == True:
                                    if volume2 > 0:
                                        prev_2 = volume2
                                        volume2 = 0
                                        set_app_volume(self.dropdown_variable2.get(), volume2)
                                    else:
                                        volume2 = prev_2
                                        set_app_volume(self.dropdown_variable2.get(), volume2)
                                elif encoder_number == 3 and volume3 != None and self.encoder3_state.get() == True:
                                    if volume3 > 0:
                                        prev_3 = volume3
                                        volume3 = 0
                                        set_app_volume(self.dropdown_variable3.get(), volume3)
                                    else:
                                        volume3 = prev_3
                                        set_app_volume(self.dropdown_variable3.get(), volume3)
                                        
            except(serial.SerialException, OSError) as e:
                self.is_thread_running = False
                self.arduino_connection = False
                self.set_switches_off()

        
        th1 = threading.Thread(target=arduino_handler, daemon=True)
        th1.start()


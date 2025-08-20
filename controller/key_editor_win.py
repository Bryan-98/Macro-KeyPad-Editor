import json
import customtkinter as ctk
from view.led_frame import LedFrame
from controller.create_key_function_frame import KeyFunctionFrame

class MacroEditor(ctk.CTkToplevel):
    def __init__(self, parent, send_data, curr_name, row, col, is_key_backlight, arduino):
        super().__init__(parent)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.title("Macro Editor")
        self.s_height = self.winfo_screenheight()
        self.s_width = self.winfo_screenwidth()

        window_width = 1066
        window_height = 600

        self.row = row
        self.col = col
        self.arduino = arduino

        self.minsize(window_width,window_height)
        self.maxsize(window_width,window_height)
        x = (self.s_width / 2) - (window_width/2)
        y = (self.s_height / 2) - (window_height/2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.after(250, lambda: self.iconbitmap('./assets/images/macro_pad_icon.ico'))
        
        self.send_data = send_data
        self.curr_name = curr_name

        self.is_key_backlight = is_key_backlight
        self.led_frame = None

        self.create_widget()


    def radiobutton_event(self, radio_var, dropdown):
        button_types = {1: getKeys('Modifiers'), 2: getKeys('Special'), 3: getKeys('Navigation'), 4: getKeys('Keypad'), 5: getKeys('Functions'), 6: getKeys('Custom')}
        newKeys = button_types[radio_var.get()]
        options = []
        for i in newKeys:
            options.append(f"{i['key']}")
        dropdown.configure(values=options)
        dropdown.set(options[0])

    def applymacro(self, m1, m2, m3, name):
        self.send_data(f'{name};{m1},{m2},{m3}')
        self.update()
        self.destroy()

    def create_widget(self):

        #Macro Key name
        if self.curr_name != None:
            holder_text = self.curr_name
        else:
            holder_text = "Enter MacroKey Name"

        self.entry = ctk.CTkEntry(self, placeholder_text=holder_text)
        self.entry.grid(row=0, column=0, columnspan=4, padx=20, pady=10)
        

        #Key function selection frames
        self.key_function_1 = KeyFunctionFrame(self)
        self.key_function_1.configure(border_width=2.5)
        self.key_function_1.grid(row=1, column=0, padx=30, pady=15, ipadx=30, ipady=20)

        self.key_function_2 = KeyFunctionFrame(self)
        self.key_function_2.configure(border_width=2.5)
        self.key_function_2.grid(row=1, column=1, padx=30, pady=15, ipadx=30, ipady=20)

        self.key_function_3 = KeyFunctionFrame(self)
        self.key_function_3.configure(border_width=2.5)
        self.key_function_3.grid(row=1, column=2, padx=30, pady=15, ipadx=30, ipady=20)

        #Led selection Frame
        if self.is_key_backlight == True:
            self.led_frame = LedFrame(self, self.row, self.col, False)
            self.led_frame.init_set_rgb(255, 0, 255)
            self.led_frame.configure(border_width=2.5)
            self.led_frame.set_arduino_connection(self.arduino)
            self.led_frame.grid(row=1, column=3, padx=30, pady=15, ipadx=30, ipady=20)
        elif self.led_frame != None:
            self.led_frame.destroy()


        # Confirmation button 
        self.submit_bttn = ctk.CTkButton(self, text="Apply", 
                                         command=lambda: self.applymacro(self.key_function_1.get_key_function(), 
                                                                         self.key_function_2.get_key_function(), 
                                                                         self.key_function_3.get_key_function(), 
                                                                         self.entry.get()))
        self.submit_bttn.grid(row=2, column=0, columnspan=4, padx=20, pady=10)

def getKeys(type):

    keys = []
    file = open('./assets/data/special_keys.json')
    data = json.load(file)

    for i in data['special_keys']:
        for j in i['keys']:
            if i['type'] == type:
                keys.append(j)
    file.close()
    return keys
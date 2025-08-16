import json, serial
import customtkinter as ctk
from controller.key_editor_win import MacroEditor
from controller.arduino_connection import send_macros_arduino, restore_saved_macros

class KeyButtonFrame(ctk.CTkFrame):
    def __init__(self, container, num_key_row, num_key_col, is_key_backlight):
        super().__init__(container)

        self.num_key_col = num_key_col
        self.num_key_row = num_key_row
        self.toplevel_window  = None
        self.received_data = None
        self.row = None
        self.col = None
        self.is_key_backlight = is_key_backlight
        self.arduino = None

        for col_index in range(self.num_key_col):
            self.grid_columnconfigure(col_index, weight=1)

        for row_index in range(self.num_key_row):
            self.grid_rowconfigure(row_index, weight=1)

        self.num_pad_text = [[None for i in range(self.num_key_col)] for j in range(self.num_key_row)]

        self.macro_keys = {}
        for key in range(self.num_key_col*self.num_key_row):
            self.macro_keys[key] = 0

        # Create a 2-d list containing a button attribute
        self.buttons = [[None for i in range(self.num_key_col)] for j in range(self.num_key_row)]

        # Iterate through the list and create a button for each row and column
        for i in range(self.num_key_row):
            for j in range(self.num_key_col):
                current_button = ctk.CTkButton(self, text=self.num_pad_text[i][j], command=lambda row=i, col=j: self.update_text(row, col))
                current_button.configure(height=80, width=80, state="disabled")
                self.buttons[i][j] = current_button
                current_button.grid(row=i, column=j, padx=10, pady=10)

    def update_text(self, row, col):

        try:
            if self.toplevel_window  is None or not self.toplevel_window.winfo_exists():
                self.row = row
                self.col = col
                self.toplevel_window  = MacroEditor(self, self.receive_data, self.buttons[row][col].cget("text"), self.row, self.col, self.is_key_backlight, self.arduino)  # create window if its None or destroyed
                self.toplevel_window.grab_set()
            else:
                self.toplevel_window.focus()  # if window exists focus it

            self.wait_window(self.toplevel_window)
        except:
            self.disable_buttons("disabled")

    def receive_data(self, data):

        def get_value(key):

            file = open('./assets/data/special_keys.json')
            data = json.load(file)

            for i in data['special_keys']:
                for j in i['keys']:
                    if j['key'] == key:
                        file.close()
                        return j['value']
            file.close()

        key_name = data.split(";")

        values = key_name[1].split(",")
        codes = []
        for i in values:
            if i != "0" or i != "":
                codes.append(str(get_value(i)))
            else:
                codes.append("000")

        btn_values = ','.join(codes)

        if btn_values != "":
            self.num_pad_text[self.row][self.col] = key_name[0]
            self.macro_keys[(self.row*self.num_key_col)+self.col] = btn_values
            self.buttons[self.row][self.col].configure(text=key_name[0])
            send_macros_arduino(self.arduino, (self.row*self.num_key_col)+self.col, btn_values)

    def get_macro_keys(self):
        return self.num_pad_text, self.macro_keys

    def set_arduino_connection(self, arduino):
        try:
            self.arduino = arduino
            self.disable_buttons("normal")
            self.restore_macros(self.macro_keys)
        except(serial.SerialException) as e:
            print("No connection to device")
            print(f'error: {e}')
    
    def disable_buttons(self, status):
        for i in range(self.num_key_row):
                for j in range(self.num_key_col):
                    self.buttons[i][j].configure(state=status)
    
    def set_macro_keys(self, numText, macroKeys):

        for i in range(self.num_key_row):
            for j in range(self.num_key_col):
                if i < len(numText) and j < len(numText[0]):
                    self.num_pad_text[i][j] = numText[i][j]
                    self.buttons[i][j].configure(text=numText[i][j])

        for i in macroKeys:
            self.macro_keys.update({int(i): macroKeys[i]})


    def restore_macros(self, macroKeys):
        saved_macros = []
        for i in macroKeys:
            saved_macros.append(macroKeys[i])

        if saved_macros[0] != 0:
            key_codes = ';'.join(saved_macros)
            restore_saved_macros(self.arduino, key_codes)

        

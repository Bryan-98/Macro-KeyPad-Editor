import json
import customtkinter as ctk
from controller.key_editor_win import MacroEditor
from controller.arduino_connection import send_macros_arduino, restore_saved_macros

class KeyButtonFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        self.toplevel_window  = None
        self.arduino = None
        self.received_data = None
        self.num_pad_text = [['0','1','2'],
                             ['3','4','5'],
                             ['6','7','8'],
                             ['9',':',';']]
        
        self.macro_keys = {
            0: '048,000,000', 1: '049,000,000', 2: '050,000,000',
            3: '051,000,000', 4: '052,000,000', 5: '053,000,000',
            6: '054,000,000', 7: '055,000,000', 8: '056,000,000',
            9: '057,000,000', 10: '058,000,000', 11: '059,000,000',
        }

        self.row = None
        self.col = None

        # Create a 2-d list containing 4 rows, 3 columns
        self.buttons = [[None for i in range(3)] for j in range(4)]

        # Iterate through the list and create a button for each row and column
        for i in range(4):
            for j in range(3):
                current_button = ctk.CTkButton(self, text=self.num_pad_text[i][j], command=lambda row=i, col=j: self.update_text(row, col))
                current_button.configure(height=80, width=80, fg_color="white", text_color="black", hover_color=("black", "lightgray"), state="disabled")
                self.buttons[i][j] = current_button
                current_button.grid(row=i, column=j, padx=10, pady=10)

    def update_text(self, row, col):

        try:
            self.arduino.read()
            if self.toplevel_window  is None or not self.toplevel_window.winfo_exists():
                self.row = row
                self.col = col
                self.toplevel_window  = MacroEditor(self, self.receive_data, self.buttons[row][col].cget("text"))  # create window if its None or destroyed
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
            if i != "0":
                codes.append(str(get_value(i)))
            else:
                codes.append("000")

        btn_values = ','.join(codes)

        if btn_values != "":
            self.num_pad_text[self.row][self.col] = key_name[0]
            self.macro_keys[(self.row*3)+self.col] = btn_values
            self.buttons[self.row][self.col].configure(text=key_name[0])
            send_macros_arduino(self.arduino, (self.row*3)+self.col, btn_values)

    def get_macro_keys(self):
        return self.num_pad_text, self.macro_keys

    def set_arduino_connection(self, arduino):
        try:
            self.arduino = arduino
            self.disable_buttons("normal")
            self.restore_macros(self.macro_keys)
        except:
            print("unabled to connect")
    
    def disable_buttons(self, status):
        for i in range(4):
                for j in range(3):
                    self.buttons[i][j].configure(state=status)
    
    def set_macro_keys(self, numText, macroKeys):

        for i in range(4):
            for j in range(3):
                self.num_pad_text[i][j] = numText[i][j]
                self.buttons[i][j].configure(text=numText[i][j])

        for i in macroKeys:
            self.macro_keys.update({int(i): macroKeys[i]})


    def restore_macros(self, macroKeys):
        saved_macros = []
        for i in macroKeys:
            saved_macros.append(macroKeys[i])
        
        key_codes = ';'.join(saved_macros)
        restore_saved_macros(self.arduino, key_codes)

        

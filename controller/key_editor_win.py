import json
import customtkinter as ctk
from tkinter import StringVar, IntVar

class MacroEditor(ctk.CTkToplevel):
    def __init__(self, parent, send_data, curr_name):
        super().__init__(parent)
        self.grid_columnconfigure((0, 1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.title("Macro Editor")
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()

        window_width = 899
        window_height = 500

        self.minsize(window_width,window_height)
        self.maxsize(window_width,window_height)
        x = (s_width / 2) - (window_width/2)
        y = (s_height / 2) - (window_height/2)
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.after(250, lambda: self.iconbitmap('./assets/images/macro_pad_icon.ico'))
        
        self.send_data = send_data
        self.curr_name = curr_name

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

        def create_button_set(radioValue, dropdown, col):
            # Create radio buttons using a loop
            i=1
            for button_type in ['Modifier', 'Special', 'Navigation', 'KeyPad', 'Function', 'Custom']:
                radio_btn = ctk.CTkRadioButton(self, text=f"{button_type}", command=lambda i = radioValue : self.radiobutton_event(i, dropdown), variable=radioValue, value=i)
                radio_btn.grid(row=i, column=col, sticky= 'w', padx=20, pady=10)
                i = i+1

        #Macro Key name
        if self.curr_name != None:
            holder_text = self.curr_name
        else:
            holder_text = "Enter MacroKey Name"

        entry = ctk.CTkEntry(self, placeholder_text=holder_text)
        entry.grid(row=0, column=1, padx=20, pady=10)

        # Dropdown 1
        macro1 = []
        dropdown_var1 = StringVar(self)
        dropdown_var1.set("0")
        dropdown1 = ctk.CTkOptionMenu(self, variable=dropdown_var1, values=macro1, dynamic_resizing=False)
        dropdown1.grid(row=7, column=0, padx=20, pady=10)        
        radio1 = IntVar(self)
        create_button_set(radio1,dropdown1,0)

        # Dropdown 2
        macro2 = []
        dropdown_var2 = StringVar(self)
        dropdown_var2.set("0")
        dropdown2 = ctk.CTkOptionMenu(self, variable=dropdown_var2, values=macro2, dynamic_resizing=False)
        dropdown2.grid(row=7, column=1, padx=20, pady=10)        
        radio2 = IntVar(self)
        create_button_set(radio2,dropdown2,1)

        # Dropdown 3
        macro3 = []
        dropdown_var3 = StringVar(self)
        dropdown_var3.set("0")
        dropdown3 = ctk.CTkOptionMenu(self, variable=dropdown_var3, values=macro3, dynamic_resizing=False)
        dropdown3.grid(row=7, column=2, padx=20, pady=10)        
        radio3 = IntVar(self)
        create_button_set(radio3,dropdown3,2)

        # Confirmation button
        ctk.CTkButton(self, text="Apply", command=lambda: self.applymacro(dropdown_var1.get(), dropdown_var2.get(), dropdown_var3.get(), entry.get())).grid(row=8, column=1, padx=20, pady=10)
      
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
import json
import customtkinter as ctk
from tkinter import StringVar, IntVar

class KeyFunctionFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.dropdown_selected = StringVar(self)

        self.create_widget()

    def radiobutton_event(self, radio_var, dropdown):
        button_types = {1: getKeys('Modifiers'), 2: getKeys('Special'), 3: getKeys('Navigation'), 4: getKeys('Keypad'), 5: getKeys('Functions'), 6: getKeys('Custom')}
        newKeys = button_types[radio_var.get()]
        options = []
        for i in newKeys:
            options.append(f"{i['key']}")
        dropdown.configure(values=options)
        dropdown.set(options[0])

    def create_widget(self):

        def create_button_set(selected_button, dropdown):
            i=1
            for button_type in ['Modifier', 'Special', 'Navigation', 'KeyPad', 'Function', 'Custom']:
                radio_btn = ctk.CTkRadioButton(self, text=f"{button_type}", command=lambda i = selected_button : self.radiobutton_event(i, dropdown), variable=selected_button, value=i)
                radio_btn.grid(row=i, column=0, sticky= 'w', padx=20, pady=10)
                i = i+1

        self.key_macro = []
        self.dropdown_selected = StringVar(self)
        self.dropdown_selected.set("")

        dropdown_options = ctk.CTkOptionMenu(self, variable=self.dropdown_selected, values=self.key_macro, dynamic_resizing=False)
        dropdown_options.grid(row=7, column=0, padx=20, pady=10)        
        selected_button = IntVar(self)
        create_button_set(selected_button,dropdown_options)

    def get_key_function(self):
        return self.dropdown_selected.get()


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
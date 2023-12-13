import serial
import time
import tkinter as tk
from tkinter import StringVar
import customtkinter as ctk

class KeyButtonFrame(ctk.CTkFrame):
    def __init__(self, container, arduino):
        super().__init__(container)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.key_editor = None
        self.arduino = arduino
        self.create_widgets()

    def create_widgets(self):

        # Create a 2-d list containing 3 rows, 4 columns
        buttons = [[None for i in range(3)] for j in range(4)]
        num_pad = [['a','b','c'],
                   ['d','e','f'],
                   ['g','h','i'],
                   ['j','k','l']] 
        
        # Iterate through the list and create a button for each row and column
        for i in range(4):
            for j in range(3):
                current_button = ctk.CTkButton(self, text=num_pad[i][j], command=lambda row=i, col=j: update_text(row, col))
                current_button.configure(height=80, width=80, fg_color="white", text_color="black", hover_color=("black", "lightgray"))
                buttons[i][j] = current_button
                current_button.grid(row=i+1, column=j+1, padx=10, pady=10)

        def update_text(row, col):

            def center_editor(size):
                s_height = self.winfo_screenheight()
                s_width = self.winfo_screenwidth()
        
                x = (s_width / 2) - (size[0]/2)
                y = (s_height / 2) - (size[1]/2)

                self.key_editor.geometry('%dx%d+%d+%d' % (size[0], size[1], x, y))
            def send(input_text):

                self.arduino.write(str.encode(f"1:[{row},{col}];{input_text}"))
                time.sleep(.05)

            if self.key_editor is None or not self.key_editor.winfo_exists():
                self.key_editor = ctk.CTkToplevel(self)
                self.key_editor.title(f"Key Editor - Key:{row},{col}")
                center_editor((711,400))
                self.key_editor.minsize(711,400)
                self.key_editor.maxsize(711,400)
                self.key_editor.grab_set()
                self.grid_columnconfigure((0, 1), weight=1)
                self.grid_rowconfigure((0, 1), weight=1)

                new_key = StringVar()
                entry = ctk.CTkTextbox(self.key_editor, width=400, corner_radius=0)
                entry.grid(row=0, column=0, padx=10, pady=10)
 
                confirm_btn = ctk.CTkButton(self.key_editor, text="Confirm", command=send(new_key))
                confirm_btn.grid(row=1, column=0, padx=10, pady=10)

                cancel_btn = ctk.CTkButton(self.key_editor, text="Cancel")
                cancel_btn.grid(row=1, column=1, padx=10, pady=10)
            else:
                self.key_editor.focus()
        
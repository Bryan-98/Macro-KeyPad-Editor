import customtkinter as ctk
from tkinter import StringVar
import time

class OnBoardConfirmation(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Save to OnBoard Memory")
        sizex= 400
        sizy = 225
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        x = (s_width / 2) - (sizex/2)
        y = (s_height / 2) - (sizy/2)
        self.geometry('%dx%d+%d+%d' % (sizex, sizy, x, y))
        self.after(250, lambda: self.iconbitmap('./assets/images/macro_pad_icon.ico'))
        
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.arduino = None
        self.msg = None
        self.confimation_msg = StringVar(self)

        self.create_widget()

    def set_connection(self, arduino):
        self.arduino = arduino

    def create_widget(self):

        def confirm_save():
            if self.arduino != None: 
                self.arduino.write(str.encode(f"3,0,0,0,0"))
                time.sleep(0.5)
                self.confimation_msg.set("Succfully saved to the onboard memory.")
                self.msg.configure(text=self.confimation_msg.get())
                self.update()
                time.sleep(1)
                self.destroy()
                
            else:
                self.msg.configure(text="Failed save to the onboard memory.")
                self.update()
                time.sleep(1)
                self.destroy()
                

        def cancel_save():
            self.update()
            self.destroy()
            

        self.confimation_msg.set("Do you want to save your current settings \nto the keypads onBoard Memeroy?")
        self.msg = ctk.CTkLabel(self, text=self.confimation_msg.get(), text_color='white', font=('Terminal', 15))
        self.msg.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        confirm_btn = ctk.CTkButton(self, text="Save", command=confirm_save)
        confirm_btn.grid(row=1, column=0, padx=5, pady=5, columnspan=1)

        cancel_btn = ctk.CTkButton(self, text="Cancel", command=cancel_save)
        cancel_btn.grid(row=1, column=1, padx=5, pady=5, columnspan=1)
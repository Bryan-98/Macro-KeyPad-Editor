import time
import customtkinter as ctk
import tkinter as tk

class LedFrame(ctk.CTkFrame):
    def __init__(self, container, arduino):
        super().__init__(container)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.arduino = arduino
        self.create_widgets()

    def create_widgets(self):
        
        def send_rgb():
            color_code = (int(red_var.get()),int(green_var.get()),int(blue_var.get()))
            self.arduino.write(str.encode(f"2:{color_code}"))
            print(f"2:{color_code}")
            time.sleep(.05)

        led = tk.Canvas(self, bg="blue", height=50, width=50)
        led.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        red_var = tk.IntVar()
        green_var = tk.IntVar()
        blue_var = tk.IntVar()
        
        red_var.set(0)
        green_var.set(251)
        blue_var.set(255)
        led.configure(bg=(f'#{int(red_var.get()):02x}{int(green_var.get()):02x}{int(blue_var.get()):02x}'))

        def change_canvas(value):
            led.configure(bg=(f'#{int(red_var.get()):02x}{int(green_var.get()):02x}{int(blue_var.get()):02x}'))

        red_color = (f'#{242:02x}{84:02x}{73:02x}')
        green_color = (f'#{55:02x}{179:02x}{55:02x}')
        blue_color = (f'#{56:02x}{64:02x}{181:02x}')

        slider_red = ctk.CTkSlider(self, from_=0, to=255, variable=red_var, orientation='vertical')
        slider_red.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=red_color, command=change_canvas)
        slider_red.grid(row=1, column=0, padx=10, pady=10)
        
        slider_green = ctk.CTkSlider(self, from_=0, to=255, variable=green_var, orientation='vertical')
        slider_green.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=green_color, command=change_canvas)
        slider_green.grid(row=1, column=1, padx=10, pady=10)
        
        slider_blue = ctk.CTkSlider(self, from_=0, to=255, variable=blue_var, orientation='vertical')
        slider_blue.configure(button_color="white",button_hover_color="darkgrey", number_of_steps=255, progress_color=blue_color, command=change_canvas)
        slider_blue.grid(row=1, column=2, padx=10, pady=10)

        apply_btn = ctk.CTkButton(self, text="Apply", command=send_rgb)
        apply_btn.configure(fg_color="white", text_color="black", hover_color=("black", "lightgray"))
        apply_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

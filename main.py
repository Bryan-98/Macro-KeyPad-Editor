import json, pystray, serial
import customtkinter as ctk
from tkinter import Menu, StringVar
from pystray import MenuItem as item
from PIL import Image
from view.encoder_frame import EncoderFrame
from view.keys_frame import KeyButtonFrame
from view.led_frame import LedFrame
from controller.save_to_onboard_win import onboard_confirmation
from controller.arduino_connection import get_device_info
from controller.com_selector_win import ComSelector
from controller.create_save_folder import init_folder, last_saved_profile, last_saved_led, last_saved_keys
from view.splash_screen_win import start_splash_win
from view.activity_frame import ActivityLight
from controller.json_file_creation import create_device_info_json
from controller.file_managment import open_file, saveas_file

class App(ctk.CTk):

    def __init__(self, title, size):
        # Main window setup
        super().__init__()
        self.title(title)

        self.center_window(size)
        self.minsize(size[0],size[1])
        self.maxsize(size[0],size[1])
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.iconbitmap("assets\images\macro_pad_icon.ico")
        
        self.selectedPort = None
        self.arduino = None
        self.msg_label = None
        self.error_msg = StringVar(self)
        self.last_saved_profile = StringVar(self)
        self.error_text = StringVar(self)

        self.key_button_widget = None
        self.led_frame = None
        self.encoder_widget = None
        self.activity_light = None
        self.onboard_confirmation = None
        self.com_selector = None
        self.splah_win = None
        self.device_entry = StringVar(self)

        self.num_keypad_row = 4
        self.num_keypad_col = 3
        self.device_info = None

        # Create a save folder and create/restore last created profile
        init_folder()
        self.last_saved_profile.set(last_saved_profile())
        
        # Run Widgets
        self.create_widget()

        #run menu
        self.create_menu()

        #system tray
        self.system_tray()

        start_splash_win(self)

    def start_selector_win(self):
        # Start com selector popup
        if self.com_selector  is None or not self.com_selector.winfo_exists():
            self.com_selector = ComSelector(self, self.selected_com)
            self.com_selector.grab_set()
        else:
            self.com_selector.focus()

        # Wait for user to select a com port
        self.wait_window(self.com_selector)

    # Get com from popup window
    def selected_com(self, data):
        self.selectedPort = data

    def restore_profile(self, data):
            try:
                led_light = data['rgb']
                macro_names = data['macroNames']
                macro_keys = data['macrosKeys']
                self.led_frame.set_rgb(led_light[0], led_light[1], led_light[2])
                self.key_button_widget.set_macro_keys(macro_names,macro_keys)
                self.key_button_widget.restore_macros(macro_keys)
            except:
                raise Exception("*   Device not connected.")
            
    def create_widget(self):

        #Device Name
        self.device_entry.set("Audio Macro Keypad")
        self.device_entry = ctk.CTkLabel(self, text=self.device_entry.get(), font=("cascadia code", 25))
        self.device_entry.grid(row=0, column=1, padx=10, pady=15, ipadx=10, ipady=20, sticky="nsew")

        #Activity Light
        self.activity_light = ActivityLight(self)
        self.activity_light.configure(border_width=2.5)
        self.activity_light.grid(row=0, column=0, padx=10, pady=10)

        # displas error message
        self.msg_label = ctk.CTkLabel(self, text=self.error_msg.get(), text_color="red")
        self.msg_label.grid(row=2, column=0, columnspan=3, padx=30, pady=15, sticky="nsew")

        #Led picker widget
        leds = last_saved_led(self.last_saved_profile.get())
        self.led_frame = LedFrame(self, 0, 0, True)
        self.led_frame.init_set_rgb(leds[0], leds[1], leds[2])
        self.led_frame.configure(border_width=2.5)
        self.led_frame.grid(row=1, column=0, padx=30, pady=15, ipadx=30, ipady=30)

        #Key buttons widget
        macro_names, macro_keys = last_saved_keys(self.last_saved_profile.get())
        self.key_button_widget = KeyButtonFrame(self,self.num_keypad_row,self.num_keypad_col, False)
        self.key_button_widget.set_macro_keys(macro_names,macro_keys)
        self.key_button_widget.configure(border_width=2.5)
        self.key_button_widget.grid(row=1, column=1, padx=30, pady=30, ipadx=30, ipady=30)
        
        #Encoder widget
        self.encoder_widget = EncoderFrame(self)
        self.encoder_widget.configure(border_width=2.5)
        self.encoder_widget.grid(row=1, column=2, padx=30, pady=30, ipadx=30, ipady=30)
        
    def create_menu(self):

        def upload_onboard():
            if self.selectedPort != None:
                onboard_confirmation(self)
            else:
                self.error_msg.set("*   Macro KeyPad not connected, can not upload to onboard memory")
                self.msg_label.configure(text=self.error_msg.get())

        def connect_to_keypad():
            try:
                self.start_selector_win()
                self.arduino = serial.Serial(port=self.selectedPort, baudrate=9600, timeout=0.1)
                device_info()
                if self.device_info['deviceName'] != "":
                    self.led_frame.set_arduino_connection(self.arduino)

                    self.device_entry.configure(text=self.device_info['deviceName'])

                    if self.device_info['audioController'] == True:
                        self.encoder_widget.set_arduino_connection(self.arduino)
                    else:
                        encoder_visibility(self.device_info['audioController'])

                    if self.device_info['keyRow'] != self.num_keypad_row and self.device_info['keyCol'] != self.num_keypad_col: 
                        resize_button_matrix(self.device_info['keyRow'], self.device_info['keyCol'], self.device_info['ledKeys'])

                    self.key_button_widget.set_arduino_connection(self.arduino)
                    self.error_msg.set("")
                    self.msg_label.configure(text=self.error_msg.get())
                    self.activity_light.set_activity_status(True)
                else:
                    self.error_msg.set("*   Device not Compatible. Please check device firmware or connection.")
                    self.msg_label.configure(text=self.error_msg.get())
                    self.activity_light.set_activity_status(False)

            except(serial.SerialException) as e:
                self.error_msg.set("*   Macro KeyPad not connected")
                self.msg_label.configure(text=self.error_msg.get())
                self.activity_light.set_activity_status(False)

        def encoder_visibility(is_visible):
            try:
                if is_visible == False:
                    self.encoder_widget.grid_forget()
                else:
                    self.encoder_widget.grid(row=0, column=2, padx=30, pady=30, ipadx=20, ipady=20)
            except():
                print("No widget Found")

        def resize_button_matrix(num_row, num_col, keyLed):
            try:
                self.key_button_widget.destroy()
                self.key_button_widget = KeyButtonFrame(self,num_row,num_col, keyLed)
                self.key_button_widget.configure(border_width=2.5)
                self.key_button_widget.grid(row=1, column=1, padx=30, pady=30, ipadx=30, ipady=30)
                self.key_button_widget.update_idletasks()
            except():
                print("Key Matrix could not be created")

        def device_info():
            try:
                if self.arduino != None:
                    data = get_device_info(self.arduino)
                    self.device_info = json.loads(create_device_info_json(data))

            except(serial.SerialException) as e:
                print("\nDevice not connected")
                

        def get_file():
            try:
                data = open_file(self.selectedPort, self.device_info)
                self.restore_profile(data)
                self.error_msg.set("")
                self.msg_label.configure(text=self.error_msg.get())
            except Exception as e:
                self.error_msg.set(e)
                self.msg_label.configure(text=self.error_msg.get())

        def save_file():
            ledLights = self.led_frame.get_rgb()
            macroNames, macrosKeys = self.key_button_widget.get_macro_keys()
            deviceId = self.device_info["deviceId"]
            saveas_file(ledLights, macroNames, macrosKeys, deviceId)

        def quit_program():
            self.encoder_widget.stop_encoder_thread()
            self.quit()

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=get_file)
        filemenu.add_command(label="Save as...", command=save_file)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=quit_program)
        menubar.add_cascade(label="File", menu=filemenu)

        arduinomenu = Menu(menubar, tearoff=0)
        arduinomenu.add_command(label="Connect", command=connect_to_keypad)
        arduinomenu.add_command(label="Upload", command=upload_onboard)
        arduinomenu.add_command(label="Device Info", command=device_info)
        menubar.add_cascade(label="KeyPad", menu=arduinomenu)
 
        self.config(menu=menubar)

    def system_tray(self):

        def quit_window(icon, item):
            icon.stop()
            self.destroy()

        def show_window(icon, item):
            icon.stop()
            self.after(0,self.deiconify)

        def hid_window():
            self.withdraw()
            image=Image.open("assets\images\macro_pad_icon.ico")
            menu=(item('Show', show_window),item('Quit', quit_window))
            icon=pystray.Icon("name", image, "KeyPad Editor", menu)
            icon.run()

        self.protocol("WM_DELETE_WINDOW", hid_window)

    def center_window(self, size):
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        
        x = (s_width / 2) - (size[0]/2)
        y = (s_height / 2) - (size[1]/2)

        self.geometry('%dx%d+%d+%d' % (size[0], size[1], x, y))

if __name__ == "__main__":

    ctk.set_default_color_theme("assets/themes/default_theme.json")
    app = App('KeyPad Editor', (1423,800))
    app.mainloop()
    
    
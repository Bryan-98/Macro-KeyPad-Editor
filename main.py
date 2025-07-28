import json, pystray, serial
import customtkinter as ctk
from tkinter import Menu, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pystray import MenuItem as item
from PIL import Image
from view.encoder_frame import EncoderFrame
from view.keys_frame import KeyButtonFrame
from view.led_frame import LedFrame
from controller.save_to_onboard_win import OnBoardConfirmation
from controller.arduino_connection import get_device_info
from model.custom_profile import create_user_profile
from controller.com_selector_win import ComSelector
from controller.create_save_folder import init_folder, last_saved_profile, last_saved_led, last_saved_keys
from view.splash_screen_win import SplashScreen
from view.activity_frame import ActivityLight

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

        self.default_num_keypad_row = 3
        self.default_num_keypad_col = 4

        self.start_splash_win()

        # Create a save folder and create/restore last created profile
        init_folder()
        self.last_saved_profile.set(last_saved_profile())
        
        # Run Widgets
        self.create_widget()

        #run menu
        self.create_menu()

        #system tray
        self.system_tray()

    def start_splash_win(self):
        # Start the splash window and close after 3 seconds
        if self.splah_win  is None or not self.splah_win.winfo_exists():
            self.splah_win = SplashScreen(self)
            self.splah_win.after(3000, lambda:self.splah_win.destroy())
        else:
            self.splah_win.focus()

        # Wait for window to close
        self.wait_window(self.splah_win)

    def start_selector_win(self):
        # Start com selector popup before main window starts
        if self.com_selector  is None or not self.com_selector.winfo_exists():
            self.com_selector = ComSelector(self, self.selected_com)
            self.com_selector.grab_set()
        else:
            self.com_selector.focus()

        # Wait for user to select a comport
        self.wait_window(self.com_selector)

    # Get com from popup window
    def selected_com(self, data):
        self.selectedPort = data

    def restore_profile(self, file):
        if file is not None:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            led_light = data['RGB']
            macro_names = data['macroNames']
            macro_keys = data['macrosKeys']

            self.led_frame.set_rgb(led_light[0], led_light[1], led_light[2])
            self.key_button_widget.set_macro_keys(macro_names,macro_keys)
            self.key_button_widget.restore_macros(macro_keys)

    def retry_widget(self):
        #Label
        error_frame = ctk.CTkLabel(self, text=self.error_text.get(), text_color='white', font=('Terminal', 30))
        error_frame.grid(row=0, column=1)

    def create_widget(self):

        #Device Name
        self.device_entry.set("Audio Macro Keypad")
        self.device_entry = ctk.CTkLabel(self, text=self.device_entry.get(), font=("cascadia code", 25))
        self.device_entry.grid(row=0, column=0, columnspan=2, padx=10, pady=15, ipadx=10, ipady=20)

        #Activity Light
        self.activity_light = ActivityLight(self)
        self.activity_light.grid(row=0, column=2, padx=10, pady=10)

        # displas error message
        self.msg_label = ctk.CTkLabel(self, text=self.error_msg.get(), text_color="red")
        self.msg_label.grid(row=2, column=0, columnspan=3, padx=30, pady=15, sticky='s')

        #Led picker widget
        leds = last_saved_led(self.last_saved_profile.get())
        self.led_frame = LedFrame(self, 2)
        self.led_frame.init_set_rgb(leds[0], leds[1], leds[2])
        self.led_frame.configure(border_width=2.5)
        self.led_frame.grid(row=1, column=0, padx=30, pady=15, ipadx=30, ipady=30)

        #Key buttons widget
        macro_names, macro_keys = last_saved_keys(self.last_saved_profile.get())
        self.key_button_widget = KeyButtonFrame(self,self.default_num_keypad_row,self.default_num_keypad_col, False)
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
                if self.onboard_confirmation  is None or not self.onboard_confirmation.winfo_exists():
                    self.onboard_confirmation = OnBoardConfirmation(self)
                    self.onboard_confirmation.set_connection(self.arduino)
                    self.onboard_confirmation.grab_set()
                else:
                    self.onboard_confirmation.focus()  # if window exists focus it

                self.wait_window(self.onboard_confirmation)
            else:
                self.error_msg.set("*   Macro KeyPad not connected, can not upload to onboard memory")
                self.msg_label.configure(text=self.error_msg.get())

        def connect_to_keypad():
            try:
                self.start_selector_win()
                self.arduino = serial.Serial(port=self.selectedPort, baudrate=9600, timeout=0.1)
                self.led_frame.set_arduino_connection(self.arduino)
                self.encoder_widget.set_arduino_connection(self.arduino)
                self.key_button_widget.set_arduino_connection(self.arduino)
                self.error_msg.set("")
                self.msg_label.configure(text=self.error_msg.get())
                self.activity_light.set_activity_status(True)
                #check_keypad_connection()

            except(serial.SerialException) as e:
                self.error_msg.set("*   Macro KeyPad not connected")
                self.msg_label.configure(text=self.error_msg.get())
                self.activity_light.set_activity_status(False)

        def encoder_visibility(is_visible):
            try:
                if bool(is_visible) == False:
                    self.encoder_widget.grid_forget()
                else:
                    self.encoder_widget.grid(row=0, column=2, padx=30, pady=30, ipadx=20, ipady=20)
            except():
                print("No widget Found")

        def device_info():
            try:
                device_info = get_device_info(self.arduino)
                print(device_info)
            except(serial.SerialException) as e:
                print(e)
                print("\nDevice not connected")
                

        def open_file():
            if self.selectedPort != None:
                file = askopenfilename(filetypes =[('Json File', '*.json')])
                try:
                    self.restore_profile(file)
                except(serial.SerialException) as e:
                    self.error_msg.set("*   Macro KeyPad not connected, can not load profile")
                    self.msg_label.configure(text=self.error_msg.get())
            else:
                self.error_msg.set("*   Macro KeyPad not connected, can not load profile")
                self.msg_label.configure(text=self.error_msg.get())

        def saveas_file():
            files = [('Json File', '*.json')]
            filepath = asksaveasfilename(filetypes = files, defaultextension = files)

            led_lights = self.led_frame.get_rgb()
            macroNames, macrosKeys = self.key_button_widget.get_macro_keys()

            profile = create_user_profile(led_lights, macroNames, macrosKeys)

            if filepath != "":
                file_write = open(filepath, mode = 'w')
                file_write.write(profile)
                file_write.close()

        def quit_program():
            self.encoder_widget.stop_encoder_thread()
            self.quit()

        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=open_file)
        filemenu.add_command(label="Save as...", command=saveas_file)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=quit_program)
        menubar.add_cascade(label="File", menu=filemenu)

        arduinomenu = Menu(menubar, tearoff=0)
        arduinomenu.add_command(label="Connect", command=connect_to_keypad)
        arduinomenu.add_command(label="Upload", command=upload_onboard)
        arduinomenu.add_command(label="Device Info", command=device_info)
        menubar.add_cascade(label="KeyPad", menu=arduinomenu)

        # helpmenu = Menu(menubar, tearoff=0)
        # helpmenu.add_command(label="Help Index", command=donothing)
        # menubar.add_cascade(label="Help", menu=helpmenu)

        
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
    app = App('KeyPad Editor', (1100,619))
    app.mainloop()
    
    
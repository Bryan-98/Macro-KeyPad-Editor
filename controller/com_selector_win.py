import customtkinter as ctk
import serial.tools.list_ports
from tkinter import StringVar

class ComSelector(ctk.CTkToplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Device Selector")
        sizex= 300
        sizy = 169
        s_height = self.winfo_screenheight()
        s_width = self.winfo_screenwidth()
        x = (s_width / 2) - (sizex/2)
        y = (s_height / 2) - (sizy/2)
        self.geometry('%dx%d+%d+%d' % (sizex, sizy, x, y))
        self.after(250, lambda: self.iconbitmap('./assets/images/macro_pad_icon.ico'))


        self.com_options = None
        self.data = data
        self.selectedPort = StringVar(self)
        
        self.create_widget()

    def create_widget(self):

        def close_window():
            port_num = getPort(self, self.selectedPort)
            self.data(port_num)
            self.update()
            self.destroy()

        def option_selection(choice):
            self.selectedPort.set(choice)
            port_num = getPort(self, choice)
            self.data(port_num)

        com_port_names = []
        com_ports = serial.tools.list_ports.comports()

        for port in com_ports:
                com_port_names.append(f'{port.description}:{port.device}')
                self.selectedPort.set(com_port_names[0])

        ctk.CTkLabel(self, text="Select COM Port:").pack()
        
        self.com_options = ctk.CTkOptionMenu(self,values = com_port_names, command=option_selection, variable = self.selectedPort)
        self.com_options.pack(padx=10, pady=10)

        ctk.CTkButton(self, text="Submit", command=close_window).pack(padx=10, pady=10)

        def getPort(self, port):
            if self.selectedPort.get() != "":
                port = self.selectedPort.get().split(":")
                return port[1]
            else:
                return ""
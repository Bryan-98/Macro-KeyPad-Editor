import time

def send_macros_arduino(arduino, key, macro):
    arduino.write(str.encode(f"1,{key},{macro}"))
    time.sleep(1.5)
    
def send_rgb_values(arduino, rgb, ledType):
    arduino.write(str.encode(f"{ledType},0,{rgb}"))
    time.sleep(1.5)

def save_to_onboard(arduino):
    arduino.write(str.encode(f"3,0,0,0,0"))
    time.sleep(1.5)

def set_encoder(arduino, switchNum, buttonState):
    arduino.write(str.encode(f"4,{switchNum},{buttonState},0,0"))
    time.sleep(1.5)

def restore_saved_macros(arduino, macros):
    arduino.write(str.encode(f"5;{macros}"))
    time.sleep(1.5)

def get_saved_macros(arduino):
    arduino.write(str.encode(f"6"))
    time.sleep(1.5)

def get_device_info(arduino):
    arduino.write(str.encode(f"8,0,0,0,0"))
    time.sleep(2)
    device_info = arduino.readline().decode('utf-8').strip()
    return device_info

def read_arduino_data(arduino):
    data = arduino.readline().strip()
    return data.decode()
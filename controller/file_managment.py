import json
from tkinter.filedialog import askopenfilename, asksaveasfilename
from model.custom_profile import create_user_profile

def open_file(selectedPort, deviceInfo):
            if selectedPort != None:
                file = askopenfilename(filetypes =[('Json File', '*.json')])
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if data["deviceId"] == deviceInfo["deviceId"]:
                        return data 
                except FileNotFoundError as exc:
                    raise Exception("*   Profile not found") from exc
            else:
                raise Exception("*   Device not connected.")

def saveas_file(ledLights, macroNames, macrosKeys, deviceId):
    files = [('Json File', '*.json')]
    filepath = asksaveasfilename(filetypes = files, defaultextension = files)

    profile = create_user_profile(deviceId, ledLights, macroNames, macrosKeys)

    try:
        file_write = open(filepath, mode = 'w')
        file_write.write(profile)
        file_write.close()
    except FileNotFoundError as e:
        print("File not saved")
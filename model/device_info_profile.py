import json

def create_device_profile(deviceName, deviceId, version, numberKeys, keyROW, keyCol, audioController, numberEncoders, underGlow, ledKey, lcdScreen):
    
    profile = {
        "deviceName": deviceName,
        "deviceId": int(deviceId),
        "version": version,
        "numberKey": int(numberKeys),
        "keyRow": int(keyROW),
        "keyCol": int(keyCol),
        "audioController": bool(int(audioController)),
        "numberEncoder": int(numberEncoders),
        "underGlow": bool(int(underGlow)),
        "ledKeys": bool(int(ledKey)),
        "lcdScreen": bool(int(lcdScreen))
    }

    json_profile = json.dumps(profile, indent=3)

    return json_profile      
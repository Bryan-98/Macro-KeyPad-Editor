import json, time

def create_user_profile(deviceId, rgb, macroNames, macrosKeys):
    
    profile = {
        "deviceId": deviceId,
        "underGlow": rgb,
        "keysRgb": rgb,
        "rgb": rgb,
        "macroNames": macroNames,
        "macrosKeys" : macrosKeys
    }

    json_profile = json.dumps(profile, indent=3)

    return json_profile      
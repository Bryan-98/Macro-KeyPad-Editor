import json, time

def create_user_profile(rgb, macroNames, macrosKeys):
    
    profile = {
        "underGlow": rgb,
        "keysRgb": rgb,
        "rgb": rgb,
        "macroNames": macroNames,
        "macrosKeys" : macrosKeys
    }

    json_profile = json.dumps(profile, indent=3)

    return json_profile      
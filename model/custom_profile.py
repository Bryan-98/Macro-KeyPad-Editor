import json, time

def create_user_profile(rgb, macroNames, macrosKeys):
    
    profile = {
        "RGB": rgb,
        "macroNames": macroNames,
        "macrosKeys" : macrosKeys
    }

    json_profile = json.dumps(profile, indent=3)

    return json_profile      
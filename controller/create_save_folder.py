import os, json, glob

#Keep incase user removes default_profiles.json
default_profile = {
   "deviceId": 0,
   "rgb": [
      255,
      147,
      255
   ],
   "macroNames": [
      [
         "0",
         "1",
         "2"
      ],
      [
         "3",
         "4",
         "5"
      ],
      [
         "6",
         "7",
         "8"
      ],
      [
         "9",
         ":",
         ";"
      ]
   ],
   "macrosKeys": {
      0: "230,000,000",
      1: "049,000,000",
      2: "050,000,000",
      3: "051,000,000",
      4: "052,000,000",
      5: "053,000,000",
      6: "054,000,000",
      7: "055,000,000",
      8: "056,000,000",
      9: "057,000,000",
      10: "058,000,000",
      11: "059,000,000"
   }
}

path = './profiles'
file = 'default.json'

def init_folder():
    if not os.path.exists(path):
        os.mkdir(path)
        make_default_profile()
    else:
        if not os.path.isfile(os.path.join(path, file)):
            make_default_profile()

def make_default_profile():
    user_profile = json.dumps(default_profile, indent=3)
    with open(os.path.join(path,file), "w") as outfile:
        outfile.write(user_profile)

def last_saved_profile():
    list_of_files = glob.glob(os.path.join(path, '*json'))
    last_file = max(list_of_files, key=os.path.getctime)
    return last_file

def last_saved_led(file):
   if file is not None:
      with open(file, 'r', encoding='utf-8') as f:
         data = json.load(f)

   return data['rgb']

def last_saved_keys(file):
   if file is not None:
      with open(file, 'r', encoding='utf-8') as f:
         data = json.load(f)

   return data['macroNames'],data['macrosKeys']

    

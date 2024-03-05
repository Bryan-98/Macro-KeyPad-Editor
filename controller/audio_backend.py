#TODO add callback
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_number_of_sessions():
    sessions = AudioUtilities.GetAllSessions()
    number_of_seesions = 0
    for session in sessions:
        if session.Process and session.Process.status() == 'running':
            number_of_seesions += 1
    return number_of_seesions

def get_app_names():
    sessions = AudioUtilities.GetAllSessions()
    apps = []
    apps.append('Master Volume')

    for session in sessions:
        if session.Process and session.Process.status() == 'running':
            apps.append(session.Process.name())

    return apps

def get_app_status(session_name):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == session_name:
            return True
    return False

def get_app_volume(session_name):
    sessions = AudioUtilities.GetAllSessions()
    if session_name == 'Master Volume':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        return math.ceil(volume.GetMasterVolumeLevelScalar() * 100)
    else:
        for session in sessions:
            if session.Process and session.Process.name() == session_name:
                interface = session.SimpleAudioVolume
                return math.ceil(interface.GetMasterVolume() * 100)

def set_app_volume(session_name, db):
    sessions = AudioUtilities.GetAllSessions()
    if session_name == 'Master Volume':
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar((db/100), None)
    else:
        for session in sessions:
            if session.Process and session.Process.name() == session_name:
                volume = session.SimpleAudioVolume
                volume.SetMasterVolume((db/100), None)

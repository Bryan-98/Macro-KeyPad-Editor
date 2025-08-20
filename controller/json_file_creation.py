from model.device_info_profile import create_device_profile

def create_device_info_json(device_info):

    data = device_info.split(',')
    device_info_splits = []

    for info in data:
        device_info_splits.append(info) 

    device_data = create_device_profile(device_info_splits[0], device_info_splits[1], device_info_splits[2], device_info_splits[3], 
                                 device_info_splits[4], device_info_splits[5], device_info_splits[6], device_info_splits[7],
                                    device_info_splits[8], device_info_splits[9], device_info_splits[10])


    return device_data
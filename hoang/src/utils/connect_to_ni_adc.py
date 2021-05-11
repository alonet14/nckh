"""
get devices and connected chan connect to laptop
"""
def get_device_info():
    from nidaqmx.system import System
    from nidaqmx.system.device import Device

    system_ni_daq = System()
    sys_local = system_ni_daq.local()
    name_device = sys_local.devices.device_names

    device_local = Device(name_device[0])

    info_device = {
        "list_devices": name_device,
        "list_ports": device_local.ai_physical_chans.channel_names
    }
    return info_device

def save_config_device_in_folder(device='Dev1', port='Dev1/ai0'):
    pass

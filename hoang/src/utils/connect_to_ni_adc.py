"""
get devices and connected chan connect to laptop
"""
def get_device(name_device="Dev1"):
    import nidaqmx.system as nisys
    device = nisys.device.Device(name_device)
    return device

def get_list_ai_chan(name_device='Dev1'):
    device = get_device(name_device)
    return device.ai_physical_chans

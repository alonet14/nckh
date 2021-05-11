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

def read_multiple_data_from_an_ai_channel(name_device='Dev1', name_chans='Dev1/ai0'):
    import nidaqmx.task as task
    from nidaqmx.stream_readers import AnalogMultiChannelReader
    from nidaqmx._task_modules.in_stream import InStream
    import numpy as np
    task_read_data = task.Task('task_in_stream')
    task_read_data.ai_channels.add_ai_voltage_chan('Dev1/ai0:1')
    task_read_data.read(number_of_samples_per_channel=512)
    task_in_stream = InStream(task_read_data)
    stored_data = np.empty((2, 512))
    analog_multi_chan_reader = AnalogMultiChannelReader(task_in_stream)
    analog_multi_chan_reader.read_many_sample(data=stored_data,
                                              number_of_samples_per_channel=512)

    task_read_data.close()

def config_for_task(name_task='', frequency=1000.0, port='Dev1/ai0'):
    """

    :param name_task: name of task
    :param frequency: in Hz
    :return:
    """
    from nidaqmx.task import Task
    configed_task = Task(name_task)
    configed_task.ai_channels.add_ai_voltage_chan(port)
    configed_task.timing.cfg_samp_clk_timing(rate=frequency)

    return configed_task


def read_data_continously(port='Dev1/ai0', sample_rate=100, time_in_seconds=30, name_file=''):
    """
    :param sample_rate: in Hz
    :param time_to_seconds: in seconds
    :param file_path: path to excel file
    :return: log data to a file
    """
    import datetime
    from nidaqmx.stream_readers import AnalogSingleChannelReader
    from nidaqmx._task_modules.in_stream import InStream
    import src.utils.file_utils as file_utils
    start_time = datetime.datetime.now().timestamp()
    data_list = []
    config_task = config_for_task(name_task='Task read I signal', frequency=sample_rate, port=port)
    instream_analog_task = AnalogSingleChannelReader(InStream(config_task))

    while True:
        data_read = instream_analog_task.read_one_sample(timeout=10)
        data_list.append(data_read)
        end_time = datetime.datetime.now().timestamp()
        if (end_time - start_time) >= time_in_seconds:
            break

    config_task.close()
    file_utils.write_to_csv_file(data=data_list, name_file=name_file)






import nidaqmx.constants
import pandas as pd
import matplotlib
from nidaqmx import task

read_port_0 = 'Dev1/ai0'
read_port_1 = 'Dev1/ai1'


def check_ai_port_working(name_device='Dev1', name_port='ai0'):
    pass


def draw(x_data=[], y_data=[], x_label_name='', y_label_name=''):
    import matplotlib
    from matplotlib import pyplot as plt
    from matplotlib.artist import Artist
    fig = plt.figure()


def read_data(name_device='Dev1'):
    import nidaqmx.task
    import connect_to_ni_adc

    list_ai_chans = connect_to_ni_adc.get_list_ai_chan(name_device).channel_names
    read_data_task = nidaqmx.task.Task('read_data_task')

    name_chan = 'Dev1/ai0'
    read_data_task.ai_channels.add_ai_voltage_chan(name_chan)
    data = read_data_task.read()
    print(data)
    read_data_task.close()


def read_multiple_data_from_an_ai_channel(name_device='Dev1', name_chans='Dev1/ai0'):
    from nidaqmx import constants
    import nidaqmx.task as task
    from nidaqmx.stream_readers import AnalogMultiChannelReader
    from nidaqmx._task_modules.in_stream import InStream
    import connect_to_ni_adc
    import numpy as np
    from nidaqmx._task_modules.channels.channel import Channel
    task_read_data = task.Task('task_in_stream')
    task_read_data.ai_channels.add_ai_voltage_chan('Dev1/ai0:1')
    task_read_data.read(number_of_samples_per_channel=512)
    task_in_stream = InStream(task_read_data)
    stored_data = np.empty((2, 512))
    print(stored_data)
    analog_multi_chan_reader = AnalogMultiChannelReader(task_in_stream)
    analog_multi_chan_reader.read_many_sample(data=stored_data,
                                              number_of_samples_per_channel=512)

    print(stored_data)

    task_read_data.close()


def read_data_continously(port='Dev1/ai0', sample_rate=100, time_in_seconds=30, file_path=''):
    """
    :param sample_rate: in Hz
    :param time: in seconds
    :return: log data to a file
    """
    import time
    import datetime
    file = open(file_path)
    start_time = datetime.datetime.now().timestamp()
    data_list = []
    while True:
        with nidaqmx.task.Task as task:
            task.ai_channels.add_ai_voltage_chan(port)
            data_list.append(task.read())

        end_time = datetime.datetime.now().timestamp()
        if (end_time - start_time) >= time_in_seconds:
            break

    file.close()


# read_multiple_data_from_an_ai_channel()

import nidaqmx
import nidaqmx.task
from nidaqmx._task_modules.in_stream import InStream
from nidaqmx._task_modules.channels import Channel

task1 = task.Task("task1")
chan = Channel(task1, read_port_0)
task1.ai_channels.add_ai_voltage_chan(read_port_0)
# instream to config in_stream in task
instream_task_config = InStream(task1)
instream_task_config.channels_to_read = chan

print(task1.in_stream.channels_to_read)
print(task1.read())
task1.close()

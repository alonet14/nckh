import nidaqmx.constants
import pandas as pd
import matplotlib
from nidaqmx import task

read_port_0 = 'Dev1/ai0'
read_port_1 = 'Dev1/ai1'
win_path_data_folder = 'E:\python_project\hoang\data'


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


def write_to_excel_file(data=[], file_path=''):
    import xlwt
    excel_object = xlwt.Workbook()
    sheet1 = excel_object.add_sheet('Sheet 1')
    for index, value in enumerate(data):
        sheet1.write(0, index, value)

    excel_object.save(file_path)


def write_to_csv_file(data='', file_path=''):
    import csv
    import os.path
    if not os.path.exists(file_path):
        file1 = open(file_path, 'x')
        file1.close()

    with open(file_path, mode='w', newline="") as store_data_file:
        employee_writer = csv.writer(store_data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for ele in data:
            employee_writer.writerow([ele])

        store_data_file.close()
    return


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


def read_data_continously(port='Dev1/ai0', sample_rate=100, time_in_seconds=30, file_path=''):
    """
    :param sample_rate: in Hz
    :param time_to_seconds: in seconds
    :param file_path: path to excel file
    :return: log data to a file
    """
    import datetime
    import os
    from nidaqmx import task
    from nidaqmx.stream_readers import AnalogSingleChannelReader
    from nidaqmx._task_modules.in_stream import InStream
    import numpy as np

    if not os.path.exists(file_path):
        file = open(file_path, 'x')
        file.close()
    elif not file_path.endswith('.csv'):
        print('Not accept this file! please replace with excel (.xlsx) file')
    start_time = datetime.datetime.now().timestamp()
    data_list = []
    config_task = config_for_task(name_task='Task read I signal', frequency=sample_rate)
    instream_analog_task = AnalogSingleChannelReader(InStream(config_task))

    # config_task.start()
    while True:
        data_read = instream_analog_task.read_one_sample(timeout=10)
        data_list.append(data_read)
        end_time = datetime.datetime.now().timestamp()
        print(end_time - start_time)
        if (end_time - start_time) >= time_in_seconds:
            break

    config_task.close()
    write_to_csv_file(data_list, file_path)
    # file.close()
    print(len(data_list))


# name_file = win_path_data_folder + '\\data.csv'
# read_data_continously(sample_rate=100, time_in_seconds=10, file_path=name_file)

def delete_data_file(parent_path=''):
    import os
    from send2trash import send2trash
    for root, _dir, file_names in os.walk(parent_path):
        for file_name in file_names:
            file_path = os.path.join(parent_path, file_name)
            if os.path.exists(file_path):
                send2trash(file_path)
            else:
                print("The file does not exist")

def write_data( name_file=''):
    import pathlib

    parent_path = str(pathlib.Path(__file__).parent.parent.parent) + '\\data'
    print(parent_path)
    delete_data_file(parent_path)

    pass

write_data()

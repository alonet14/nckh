import nidaqmx.constants
import pandas as pd
import matplotlib
from nidaqmx import task


def read_data(name_device='Dev1'):
    import nidaqmx.task
    import connect_to_ni_adc

    list_ai_chans = connect_to_ni_adc.get_list_ai_chan(name_device).channel_names
    read_data_task = nidaqmx.task.Task('read_data_task')

    name_chan = 'Dev1/ai0'
    read_data_task.ai_channels.add_ai_voltage_chan(name_chan)
    data = read_data_task.read()
    read_data_task.close()


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


def write_to_csv_file(data='', name_file=''):
    import csv
    import os.path
    import pathlib
    parent_path = str(pathlib.Path(__file__).parent.parent.parent) + '\\data'
    delete_data_file(parent_path)
    if not name_file.endswith('.csv'):
        return
    file_path = os.path.join(parent_path, name_file)

    # create file
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


def read_data_continously(port='Dev1/ai0', sample_rate=100, time_in_seconds=30, name_file=''):
    """
    :param sample_rate: in Hz
    :param time_to_seconds: in seconds
    :param file_path: path to excel file
    :return: log data to a file
    """
    import datetime
    import os
    from nidaqmx.stream_readers import AnalogSingleChannelReader
    from nidaqmx._task_modules.in_stream import InStream

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
    write_to_csv_file(data=data_list, name_file=name_file)


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


import datetime
time_now = datetime.datetime.now().timestamp()
time_now = int(time_now)
name_file = ''.join(['data_at_', str(time_now), '.csv'])
read_data_continously(time_in_seconds=5, name_file=name_file)

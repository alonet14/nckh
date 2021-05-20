def read_data(name_device='Dev1'):
    import nidaqmx.task
    import connect_to_ni_adc

    list_ai_chans = connect_to_ni_adc.get_list_ai_chan(name_device).channel_names
    read_data_task = nidaqmx.task.Task('read_data_task')

    name_chan = 'Dev1/ai0'
    read_data_task.ai_channels.add_ai_voltage_chan(name_chan)
    data = read_data_task.read()
    read_data_task.close()


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
    delete_files_in_folder(parent_path)
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


def save_config_device_in_folder(device='Dev1', port='Dev1/ai0'):
    import json
    import pathlib
    import os

    config_path = os.path.join(str(pathlib.Path(__file__).parent.parent.parent), 'setting')
    delete_files_in_folder(config_path)
    info_device_to_read = {
        'device': device,
        'port': port
    }
    file_config_path = config_path + '\\config.json'
    file_config = open(file_config_path, 'w')
    json.dump(obj=info_device_to_read, fp=file_config)
    file_config.close()


def delete_files_in_folder(parent_path=''):
    import os
    from send2trash import send2trash
    for root, _dir, file_names in os.walk(parent_path):
        for file_name in file_names:
            file_path = os.path.join(parent_path, file_name)
            if os.path.exists(file_path):
                send2trash(file_path)
            else:
                print("The file does not exist")

def write_person_data(data):
    import pathlib
    import json
    path_person_data = str(pathlib.Path(__file__).parent.parent.parent) + '\\person_data'
    file_name = path_person_data + '\\data.json'
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
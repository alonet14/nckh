import pathlib
import numpy as np
from PyQt5 import QtWidgets, uic
from nidaqmx.constants import AcquisitionType, Edge
from nidaqmx.task import Task
import src.utils.file_utils as file_utils
from src.view.manual_fill import ManualFill

class DisplayHrRr(QtWidgets.QWidget):
    def __init__(self, parent):
        from nidaqmx.stream_readers import AnalogSingleChannelReader
        from nidaqmx._task_modules.in_stream import InStream
        super(DisplayHrRr, self).__init__(parent)
        ui_path = str(pathlib.Path(__file__).parent) + "\\display.ui"
        self.ui = uic.loadUi(ui_path, self)

        info = read_config_file()
        configed_task = Task('Task read I signal')
        configed_task.ai_channels.add_ai_voltage_chan(info['port'])
        configed_task.timing.cfg_samp_clk_timing(rate=100,
                                                 source=u'',
                                                 active_edge=Edge.RISING,
                                                 sample_mode=AcquisitionType.FINITE,
                                                 samps_per_chan=1500)

        self.data_raw = np.zeros(shape=(1500,))
        self.instream_analog_task = AnalogSingleChannelReader(InStream(configed_task))

        # init
        self.progress.setValue(0)
        self.init_state_button()

        self.button_auto.clicked.connect(self.button_auto_event)
        self.button_manual.clicked.connect(self.button_manual_event)
        self.button_refresh.clicked.connect(self.refresh)

        # click predict
        self.combobox_mode.addItems(["Tự động", "Thủ công"])
        self.manual_mode = False
        self.combobox_mode.currentIndexChanged.connect(self.update_mode)

        # event button
        self.button_predict.clicked.connect(self.predict)

        #thread read data temp
        import threading
        import src.utils.read_data_temp as rdt
        thread_read_data = threading.Thread(target=rdt.read_data_temp, daemon=True)
        thread_read_data.start()

    # ==================event button ================
    def init_state_button(self):
        self.button_auto.setEnabled(True)
        self.button_manual.setEnabled(False)

    def function_append_data(self):
        self.instream_analog_task.read_many_sample(data=self.data_raw, number_of_samples_per_channel=1500, timeout=100)
        self.button_auto.setEnabled(True)
        self.button_auto.setText("Tiến hành đo tự động")
        self.combobox_mode.setEnabled(True)

        # calculate
        data_raw_hr_rr = self.data_raw
        import src.utils.butterworth_filter as btwf

        hr = len(btwf.find_hr(data_raw_hr_rr))*4
        rr = len(btwf.find_rr(data_raw_hr_rr))*4

        self.label_hr.setText('Nhịp tim: ' + str(hr) + ' bpm')
        self.label_rr.setText('Nhịp thở: ' + str(rr) + ' bpm')

        parent_path = str(pathlib.Path(__file__).parent.parent.parent) + "\\data\\temp"
        file_path = parent_path + '\\temp.txt'
        with open(file_path, 'r') as file_temp:
            temp = file_temp.readline(5)
            file_temp.close()

        info = {'name': 'Default', 'hr': hr, 'rr': rr, 'temp': temp}
        file_utils.write_person_data(info)

        import matplotlib.pyplot as plt
        import numpy as np
        peaks = btwf.find_hr(self.data_raw)
        peaks2 = btwf.find_rr(self.data_raw)
        HR = btwf.butter_bandpass_filter(self.data_raw)
        RR = btwf.butter_lowpass_filter(self.data_raw)
        t = np.arange(0, 15, 0.01)
        plt.figure(2)
        plt.title('HR signal')
        plt.xlabel('Times')
        plt.ylabel('Voltage')
        plt.plot(t, HR)
        plt.plot(t[peaks], HR[peaks], 'x')
        # tín hiệu nhịp thở
        plt.figure(3)
        plt.title('RR signal')
        plt.xlabel('Times')
        plt.ylabel('Voltage')
        plt.plot(t, RR)
        plt.plot(t[peaks2], RR[peaks2], 'x')
        plt.show()



    def timer_count(self):
        timer_amount = 15  # s
        val_pro = 0
        import time
        while timer_amount > 0:
            time.sleep(1)
            val_pro += 6.67
            if val_pro >= 100:
                val_pro = 100
            timer_amount -= 1
            self.progress.setValue(int(val_pro))

    def button_auto_event(self):
        self.button_auto.setEnabled(False)
        self.button_auto.setText("Đang xử lý dữ liệu...")
        self.combobox_mode.setEnabled(False)
        self.label_hr.setText('Nhịp tim: đang xử lý dữ liệu')
        self.label_rr.setText('Nhịp thở: đang xử lý dữ liệu')

        if self.data_raw.size > 0:
            self.data_raw = np.zeros(shape=(1500,))

        # create thread and run
        import threading
        thread_append = threading.Thread(target=self.function_append_data, daemon=True)
        thread_append.start()

        thread_timer = threading.Thread(target=self.timer_count, daemon=True)
        thread_timer.start()

    def button_manual_event(self):
        self.w = ManualFill()
        self.w.show()

    def update_mode(self):
        print(self.combobox_mode.currentIndex())
        if self.combobox_mode.currentIndex() == 0:
            self.manual_mode = False
            self.button_auto.setEnabled(True)
            self.button_manual.setEnabled(False)
        else:
            self.manual_mode = True
            self.button_auto.setEnabled(False)
            self.button_manual.setEnabled(True)

    def refresh(self):
        parent_path = str(pathlib.Path(__file__).parent.parent.parent) + "\\data\\temp"
        file_path = parent_path + '\\temp.txt'
        with open(file_path, 'r') as file_temp:
            temp = file_temp.readline(5)
            file_temp.close()
        print(temp)
        self.label_temp.setText('Nhiệt độ: {}'.format(temp))

    def predict(self):
        info = read_person_data()
        assert info != None
        name = info['name']
        hr = int(info['hr'])
        rr = int(info['rr'])
        temp = float(info['temp'])
        data = [[hr, rr, temp]]

        import pathlib
        import pickle
        path_folder_model = str(pathlib.Path(__file__).parent.parent) + '\\trained_model'
        model_file_path = path_folder_model + '\\SVM.sav'
        with open(model_file_path, 'rb') as model_file:
            loaded_model = pickle.load(model_file)
            result = loaded_model.predict(data)
            print(result[0])
            model_file.close()

            if result == 1.0:
                self.label_result.setText("KẾT QUẢ: Bệnh nhân {name} bình thường".format(name=name))
            else:
                self.label_result.setText("KẾT QUẢ: Bệnh nhân {name} có khả năng bị sốt xuất huyết".format(name=name))


def get_path_data_file(type_file=True):
    """
    :param type_file: True if csv
                    False if excel file
    :return: path data file
    """

    def get_file_in_path(file_path):
        import os
        list_file = []
        for root, _dir, name_files in os.walk(file_path):
            for element in name_files:
                list_file.append(os.path.join(file_path, element))
        return list_file

    if type_file:
        pass
    else:
        path_data = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '\\data'
        return get_file_in_path(path_data)


def get_data_excel(path_data=''):
    import pandas as pd
    import numpy as np
    data = pd.read_excel(path_data, usecols='B', index_col=0)
    return np.asarray(data.index)


def read_config_file():
    import json
    import pathlib
    import os
    parent_config_file = os.path.join(str(pathlib.Path(__file__).parent.parent.parent), 'setting')
    file_config = parent_config_file.__str__() + '\\config.json'
    with open(file_config, 'r') as config_file:
        info = json.load(config_file)
        return info


def read_person_data():
    import pathlib
    import json
    path_person_data = str(pathlib.Path(__file__).parent.parent.parent) + '\\person_data'
    file_name = path_person_data + '\\data.json'
    if pathlib.Path(file_name).exists():
        with open(file_name, 'r') as json_file:
            person_data = json.load(json_file)
            return person_data
    else:
        return None

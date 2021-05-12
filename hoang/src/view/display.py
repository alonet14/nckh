import pathlib
import numpy as np
from PyQt5 import QtWidgets, uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets, is_pyqt5

if is_pyqt5():
    pass
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas)
from matplotlib.figure import Figure
from nidaqmx.task import Task




class DisplayHrRr(QtWidgets.QWidget):
    def __init__(self, parent):
        from nidaqmx.stream_readers import AnalogSingleChannelReader
        from nidaqmx._task_modules.in_stream import InStream

        super(DisplayHrRr, self).__init__(parent)
        ui_path = str(pathlib.Path(__file__).parent) + "\\display.ui"
        self.ui = uic.loadUi(ui_path, self)
        self.data_raw = [0 for i in range(1001)]
        self.data_raw_to_show_hr_rr = []

        info = read_config_file()
        configed_task = Task('Task read I signal')
        configed_task.ai_channels.add_ai_voltage_chan(info['port'])
        configed_task.timing.cfg_samp_clk_timing(rate=100)

        self.config_task = configed_task
        self.instream_analog_task = AnalogSingleChannelReader(InStream(self.config_task))

        # create thread and run
        self.thread_append_to_raw_data()

        # show diagram
        self.show_hr_diagram()
        self.show_rr_diagram()

        self.thread_calculate_hr()
        # show result hr rr
        # self.show_hr()
        # self.show_rr()

    def function_append_to_raw_data(self):
        self.data_raw.pop(0)
        if len(self.data_raw_to_show_hr_rr) >= 6002:
            self.data_raw_to_show_hr_rr.pop(0)
        self.config_task.start()
        data_read_from_ni_adc = self.instream_analog_task.read_one_sample(timeout=10)
        self.data_raw.append(data_read_from_ni_adc)
        self.data_raw_to_show_hr_rr.append(data_read_from_ni_adc)
        self.config_task.stop()

    def thread_append_to_raw_data(self):
        import continuous_threading
        thread_append = continuous_threading.ContinuousThread(target=self.function_append_to_raw_data, daemon=True)
        thread_append.start()

    def function_calculate_hr(self):
        if len(self.data_raw_to_show_hr_rr) >= 6000:
            data_raw = self.data_raw_to_show_hr_rr[-6000:]
            import src.utils.butterworth_filter as btwf
            hr = len(btwf.find_hr(data_raw))
            rr = len(btwf.find_rr(data_raw))
            self.label_hr.setText('Nhịp tim: ' + str(hr) + ' bpm')
            self.label_rr.setText('Nhịp thở: ' + str(rr) + ' bpm')
        else:
            print('running')
            self.label_hr.setText('Nhịp tim: đang xử lý dữ liệu')
            self.label_rr.setText('Nhịp thở: đang xử lý dữ liệu')

    def thread_calculate_hr(self):
        import continuous_threading
        thread_calculate = continuous_threading.ContinuousThread(target=self.function_calculate_hr, daemon=True)
        thread_calculate.start()

    def show_hr_diagram(self):
        layout = QtWidgets.QVBoxLayout(self.widget_hr)
        dynamic_canvas_hr = FigureCanvas(Figure(figsize=(2, 2), dpi=80))
        layout.addWidget(dynamic_canvas_hr)
        self._dynamic_ax_hr = dynamic_canvas_hr.figure.subplots()
        self._timer_hr = dynamic_canvas_hr.new_timer(
            10, [(self._update_canvas_hr, (), {})])
        self._timer_hr.start()

    def _update_canvas_hr(self):
        import src.utils.butterworth_filter as bwft
        self._dynamic_ax_hr.clear()
        t = np.linspace(0, 10, 1000)
        read_data = self.data_raw[-1000:]
        handled_data = np.array(bwft.butter_bandpass_filter(read_data))
        self._dynamic_ax_hr.plot(t, handled_data, '.')
        self._dynamic_ax_hr.set_ylim([-3.5, 3.5])
        self._dynamic_ax_hr.figure.canvas.draw()

    def show_rr_diagram(self):
        layout = QtWidgets.QVBoxLayout(self.widget_rr)
        dynamic_canvas_rr = FigureCanvas(Figure(figsize=(2, 2), dpi=80))
        layout.addWidget(dynamic_canvas_rr)
        self._dynamic_ax_rr = dynamic_canvas_rr.figure.subplots()
        self._timer_rr = dynamic_canvas_rr.new_timer(
            10, [(self._update_canvas_rr, (), {})])
        self._timer_rr.start()

    def _update_canvas_rr(self):
        import src.utils.butterworth_filter as bwft
        self._dynamic_ax_rr.clear()
        t = np.linspace(0, 10, 1000)
        read_data = self.data_raw[-1000:]
        handled_data = np.array(bwft.butter_lowpass_filter(read_data))
        self._dynamic_ax_rr.plot(t, handled_data, '.', )
        self._dynamic_ax_rr.set_ylim([-3.5, 3.5])
        self._dynamic_ax_rr.figure.canvas.draw()

    def show_hr(self):
        import src.utils.butterworth_filter as butterworth_filter
        path_data = get_path_data_file(type_file=False)
        label_hr = self.label_hr
        label_hr.setText("Đang xử lý .")
        data_raw = get_data_excel(path_data[0])
        handled_data = butterworth_filter.find_hr(data_raw)
        hr = str(handled_data.size) + ' bpm'

        pass

    def show_rr(self):
        import src.utils.butterworth_filter as butterworth_filter
        path_data = get_path_data_file(type_file=False)
        label_rr = self.label_rr
        label_rr.setText("Đang xử lý .")
        data_raw = get_data_excel(path_data[0])
        handled_data = butterworth_filter.find_rr(data_raw)
        hr = str(handled_data.size) + ' bpm'
        pass


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
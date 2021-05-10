from PyQt5 import QtWidgets, uic
import sys
from src.controller.setup_controller import *
import pathlib

from src.view.display import DisplayHrRr

class MainWindow(QtWidgets.QMainWindow):
    def __init(self):
        super(MainWindow, self).__init()
        ui_path = str(pathlib.Path(__file__).parent) + "\\main_window.ui"
        uic.loadUi(ui_path, self)
        # self.centralWidget.setFixedWidth(800)
        # self.centralWidget.setFixedHeight(600)

class Setup(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Setup, self).__init__(parent)

        ui_path = str(pathlib.Path(__file__).parent) + "\\setup.ui"

        uic.loadUi(ui_path, self)

        # ==================Config==================
        # ======Name=====
        self.setup_list_device()
        self.setup_list_port()

        # =====Button====
        self.button_check_device.clicked.connect(self.check_device_active_event)
        self.button_check_port.clicked.connect(self.check_port_working_event)
        self.button_hr_rr.clicked.connect(self.go_to_hr_rr_page)

    def get_parent(self):
        return self.parent()

    def setup_list_device(self, data=['Dev1', 'Dev2']):
        set_item_for_commbo_box(data, self.combobox_devices)
        pass

    def setup_list_port(self, name_device='Dev1'):
        data = ['ai0', 'ai1', 'ai2']
        concatenated_data = map(lambda ele: name_device + '/' + ele, data)
        set_item_for_commbo_box(concatenated_data, self.combobox_ports)

    def check_device_active_event(self):
        choice = self.combobox_devices.currentText()
        print(choice)

    def check_port_working_event(self):
        choice = self.combobox_ports.currentText()
        print(choice)

    def go_to_hr_rr_page(self):
        window = self.get_parent()
        display_widget = DisplayHrRr(window)
        self.close()
        display_widget.show()






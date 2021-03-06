from PyQt5 import QtWidgets, uic
from src.controller.setup_controller import *
import pathlib
from src.view.display import DisplayHrRr
import src.utils.connect_to_ni_adc as connect_to_ni_adc


class MainWindow(QtWidgets.QMainWindow):
    def __init(self):
        super(MainWindow, self).__init()
        ui_path = str(pathlib.Path(__file__).parent) + "\\main_window.ui"
        uic.loadUi(ui_path, self)


class Setup(QtWidgets.QWidget):
    def __init__(self, parent):
        super(Setup, self).__init__(parent)

        ui_path = str(pathlib.Path(__file__).parent) + "\\setup.ui"

        uic.loadUi(ui_path, self)

        # ==================Config==================
        info_device = connect_to_ni_adc.get_device_info()
        # ======Name=====
        self.setup_list_device(info_device=info_device)
        self.setup_list_port(info_device=info_device)

        # =====Button====
        self.button_check_device.clicked.connect(self.check_device_active_event)
        self.button_check_port.clicked.connect(self.check_port_working_event)
        self.button_hr_rr.clicked.connect(self.go_to_hr_rr_page)

    def get_parent(self):
        return self.parent()

    def setup_list_device(self, info_device={}):
        name_device = info_device['list_devices']
        set_item_for_commbo_box(name_device, self.combobox_devices)

    def setup_list_port(self, info_device):
        name_ai_physical_channel = info_device['list_ports']
        set_item_for_commbo_box(name_ai_physical_channel, self.combobox_ports)

    def check_device_active_event(self):
        choice = self.combobox_devices.currentText()
        print(choice)

    def check_port_working_event(self):
        choice = self.combobox_ports.currentText()
        print(choice)

    def go_to_hr_rr_page(self):
        # create config file
        import src.utils.file_utils as file_utils
        device = self.combobox_devices.currentText()
        port = self.combobox_ports.currentText()
        file_utils.save_config_device_in_folder(device=device, port=port)

        window = self.get_parent()
        self.close()

        display_widget = DisplayHrRr(window)
        display_widget.show()

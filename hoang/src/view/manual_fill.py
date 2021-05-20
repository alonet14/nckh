import pathlib
from PyQt5 import uic, QtWidgets
import src.utils.file_utils as file_utils

class ManualFill(QtWidgets.QMainWindow):
    def __init__(self):
        super(ManualFill, self).__init__()
        ui_path = str(pathlib.Path(__file__).parent) + '\\manual_fill.ui'
        uic.loadUi(ui_path, self)

        self.button_confirm.setText('Xác nhận')
        self.button_confirm.clicked.connect(self.confirm)

    def get_info(self):
        name = self.line_edit_name.text()
        hr = self.line_edit_hr.text()
        rr = self.line_edit_rr.text()
        temp = self.line_edit_temp.text()
        return {'name': name, 'hr': hr, 'rr': rr, 'temp': temp}

    def confirm(self):
        info = self.get_info()
        file_utils.write_person_data(info)
        self.button_confirm.setText('Ghi thành công. Vui lòng chờ')

        self.close()

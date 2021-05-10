from PyQt5 import QtCore, QtGui, QtWidgets


def name_software(label=QtWidgets.QLabel, name=''):
    label.setText(name)


def set_item_for_commbo_box(data=['Dev1', 'Dev2'], combobox=QtWidgets.QComboBox):
    for index, value in enumerate(data):
        combobox.addItem(value)



def get_list_ai_port(name_device):
    data = ['demo']
    pass

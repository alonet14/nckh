import sys
from PyQt5 import QtWidgets
from src.view.display import DisplayHrRr
from src.view.setup import Setup, MainWindow

if __name__ == "__main__":
    name_window = 'Phần mềm đo nhịp tim và nhịp thở'
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setFixedWidth(800)
    window.setFixedHeight(600)
    setup_screen = Setup(window)

    window.setWindowTitle(name_window)
    window.show()
    app.exec_()

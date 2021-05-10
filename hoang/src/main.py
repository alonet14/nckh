import sys
from PyQt5 import QtWidgets
from src.view.display import DisplayHrRr
from src.view.setup import Setup, MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    window.setFixedWidth(800)
    window.setFixedHeight(600)
    setup_screen = Setup(window)
    window.show()
    app.exec_()

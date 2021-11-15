from main_classes import Viewer as v
from PyQt5 import QtWidgets

import sys


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.widget = v.Viewer()
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.addWidget(self.widget)
        self.setLayout(mainLayout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QMainWindow()
    ui = MainWindow(Form)
    ui.show()
    sys.exit(app.exec_())

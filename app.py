import sys

from PyQt5 import QtWidgets

from windows.functionality.main import Main_window

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Main_window()
    w.show()
    sys.exit(app.exec_())

from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = sermonconvert.ui.MainWindow()
    window.show()
    app.exec_()


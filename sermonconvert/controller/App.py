from PyQt5 import QtWidgets
import sys

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = sermonconvert.ui.MainWindow()

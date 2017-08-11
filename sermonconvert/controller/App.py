from PyQt5 import QtWidgets
from sermonconvert.ui.SCMainWindow import SCMainWindow
import sys

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = SCMainWindow()
        self.main_view.show()

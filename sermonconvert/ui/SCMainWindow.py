from PyQt5 import QtWidgets, QtCore
from sermonconvert.qt.gen_MainWindow import Ui_MainWindow
from sermonconvert.model.ffmpeg import FFMpeg
import os
import sys
import re
import math

class SCMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(SCMainWindow, self).__init__(parent)
        self.setupUi()
        self.filename = ""

    def setupUi(self):
        super(SCMainWindow, self).setupUi(self)
        self.chooseFileButton.clicked.connect(self.chooseFileDialog)
        self.convertButton.clicked.connect(self.convertFile)

        self.sermonDate.dateChanged.connect( self.derive_outputfilename )
        self.seriesTitle.textEdited.connect( self.derive_outputfilename )
        self.sequenceNumber.valueChanged.connect( self.derive_outputfilename )
        self.sermonTitle.textEdited.connect( self.derive_outputfilename )

    def chooseFileDialog(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(
            caption = "Choose source video file",
            directory = os.path.expanduser('~'),
            filter = "Videos (*.mp4 *.mov *.avi *.m4v)"
        )[0]
        self.labelFileName.setText(self.filename);

    def starttime(self):
        return self.timeStart.time().toString('hh:mm:ss')

    def duration(self):
        return self.timeDuration.time().toString('hh:mm:ss')

    def sermondate(self):
        return self.sermonDate.date().toString('yyyy-MM-dd')

    def seriesName(self):
        return self.seriesTitle.text()

    def seqNum(self):
        return self.sequenceNumber.value()

    def sermonName(self):
        return self.sermonTitle.text()

    def derive_outputfilename(self):
        self.outputFile.setText( "%s %s %d - %s.mp4" % (
            self.sermondate(), self.seriesName(),
            self.seqNum(), self.sermonName())
        )

    def outputfilename(self):
        return self.outputFile.text()

    def updateProgress(self, text):
        # Update progress bar
        self.operationProgress.setValue(self.process.percent)
        self.overallProgress.setValue(self.process.percent)

        # Add to the log window
        cursor = self.outputWindow.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.outputWindow.ensureCursorVisible()

    def convertFile(self):
        self.process = FFMpeg(
            input_file = self.filename,
            output_file = self.outputfilename(),
            start_time_tc = self.starttime(),
            duration_tc = self.duration(),
            )
        self.process.started.connect( lambda: self.convertButton.setEnabled(False) )
        self.process.incoming_data.connect( self.updateProgress )
        self.process.finished.connect( lambda: self.convertButton.setEnabled(True) )
        self.process.convertFile()



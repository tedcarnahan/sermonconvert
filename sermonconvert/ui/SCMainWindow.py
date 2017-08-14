from PyQt5 import QtWidgets, QtCore
from sermonconvert.qt.gen_MainWindow import Ui_MainWindow
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

        self.process = QtCore.QProcess(self)
        self.process.readyRead.connect(self.dataReady)
        self.process.started.connect( lambda: self.convertButton.setEnabled(False) )
        self.process.finished.connect( lambda: self.convertButton.setEnabled(True) )

    def dataReady(self):
        text_from_process = str(self.process.readAll(), 'utf-8')

        # Update progress bar
        self.updateProgress(text_from_process)

        # Add to the log window
        cursor = self.outputWindow.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text_from_process)
        self.outputWindow.ensureCursorVisible()

    def timecode_to_secs(self, time_str):
        m = re.search("(\d\d):(\d\d):(\d\d\.?\d?\d?)", time_str)
        return int(m[1])*3600 + int(m[2])*60 + math.ceil(float(m[3]))

    def updateProgress(self, logtext):
        m = re.search("time=(\d\d:\d\d:\d\d\.\d\d)", logtext)
        if m:
            curtime_s = self.timecode_to_secs(m[1])
            durtime_s = self.timecode_to_secs(self.duration())
            percent = curtime_s / durtime_s * 100
            self.operationProgress.setValue(int(percent))
            self.overallProgress.setValue(int(percent))
        
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

    def outputfilename(self):
        return "%s %s %d - %s.mp4" % (
            self.sermondate(), self.seriesName(),
            self.seqNum(), self.sermonName())

    def convertFile(self):
        print(self.outputfilename())

        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.process.start('/usr/local/bin/ffmpeg', [
            '-report',
            '-fflags', '+genpts',
            '-ss', self.starttime(),
            '-i', self.filename,
            '-to', self.duration(),
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-c:a', 'copy',
            '-pix_fmt', 'yuv420p',
            self.outputfilename()
        ])


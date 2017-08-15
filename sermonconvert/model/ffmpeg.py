from PyQt5 import QtCore
from sermonconvert.util import timecode_to_secs
import re

class FFMpeg(QtCore.QProcess):

    percentChanged = QtCore.pyqtSignal()
    incoming_data = QtCore.pyqtSignal(str)

    def __init__(self, input_file="", output_file="", start_time_tc="", duration_tc=""):
        QtCore.QProcess.__init__(self)
        self.input_file = input_file
        self.output_file = output_file
        self.start_time_tc = start_time_tc
        self.duration_tc = duration_tc
        self.percent = 0

    def incoming_data_emitter(self):
        text = str(self.readAll(), 'utf-8')
        self.incoming_data.emit(text)

    def update_percent(self, text):
        m = re.search("time=(\d\d:\d\d:\d\d\.\d\d)", text)
        if m:
            curtime_s = timecode_to_secs(m[1])
            durtime_s = timecode_to_secs(self.duration_tc)
            self.percent = curtime_s / durtime_s * 100
            self.percentChanged.emit()

    def convertFile(self, started_cb=None, progress_cb=None, finished_cb=None):
        self.setProcessChannelMode( QtCore.QProcess.MergedChannels )
        self.readyRead.connect( self.incoming_data_emitter )
        self.incoming_data.connect( lambda text: self.update_percent(text) )
        self.start('/usr/local/bin/ffmpeg', [
            '-y',
            '-report',
            '-fflags', '+genpts',
            '-ss', self.start_time_tc,
            '-i', self.input_file,
            '-to', self.duration_tc,
            '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
            '-c:a', 'copy',
            '-pix_fmt', 'yuv420p',
            self.output_file
        ])

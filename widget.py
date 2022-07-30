# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QPushButton, QTextEdit, QSlider

import time
import json
import serial
from pprint import pprint
import random

ser  = serial.Serial("COM5", baudrate= 9600,
       timeout=2.5,
       parity=serial.PARITY_NONE,
       bytesize=serial.EIGHTBITS,
       stopbits=serial.STOPBITS_ONE
    )


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()
        self.btnReadData = self.findChild(QPushButton, "btnReadData")
        self.btnSetting = self.findChild(QPushButton, "btnSetting")
        self.tbxHighTemperature = self.findChild(QTextEdit, "tbxHighTemperature");
        self.tbxLowTemperature = self.findChild(QTextEdit, "tbxLowTemperature");
        self.tbxNowTemperature = self.findChild(QTextEdit, "tbxNowTemperature");
        self.hzsSpeedFan = self.findChild(QSlider, "hzsSpeedFan");
#        self.timer = QTimer()
#        self.timer.timeout.connect(self.ReadDataSensor)
#        self.timer.start(1000)

        self.btnReadData.clicked.connect(self.ReadDataSensor)
        self.btnSetting.clicked.connect(self.SendSetting)
        self.tbxHighTemperature.setPlainText("30")
        self.tbxLowTemperature.setPlainText("30")


    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def Change2Start(self):
        data = {}
        data["status"] = "start"
        data=json.dumps(data)
        print (data)
        if ser.isOpen():
            ser.write(data.encode('ascii'))
            ser.flush()

    def Change2Stop(self):
        data = {}
        data["status"] = "stop"
        data=json.dumps(data)
        print (data)
        if ser.isOpen():
            ser.write(data.encode('ascii'))
            ser.flush()

    def SendSetting(self):
        data = {}
        data["data1"] = 0 + int(self.tbxHighTemperature.toPlainText())
        data["data2"] = 0 + int(self.tbxLowTemperature.toPlainText())
        data["data3"] = 2 * self.hzsSpeedFan.value()
        data=json.dumps(data)
        print (data)
        if ser.isOpen():
            ser.write(data.encode('ascii'))
            ser.flush()

    def ReadDataSensor(self):
        global ser
        serialLine = "";
        if ser.isOpen():
            serialLine = ser.read(100).decode('ascii').split("{")
            serialLine = "{" + serialLine[1].split("}")[0] + "}"

            dataTemperature = json.loads(serialLine)
            self.tbxNowTemperature.setPlainText(str(round(dataTemperature.get("temperature"),2)) + " *C")

print ("Ready...")





if __name__ == "__main__":

    app = QApplication([])
    widget = Widget()

    widget.show()
    sys.exit(app.exec_())


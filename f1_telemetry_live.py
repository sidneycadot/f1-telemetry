 #! /usr/bin/env python3

import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtNetwork, QtGui

from f1_telemetry_dtype import F1_2017_UDPPacket

app = None

class CentralWidget(QtWidgets.QWidget):

    fields = [
        ('time'           , 'm_time'          , lambda x: '{:.1f}'.format(x)       , 's'   ),
        ('lap time'       , 'm_lapTime'       , lambda x: '{:.1f}'.format(x)       , 's'   ),
        ('lap distance'   , 'm_lapDistance'   , lambda x: '{:.1f}'.format(x)       , 'm'   ),
        ('total distance' , 'm_totalDistance' , lambda x: '{:.1f}'.format(x)       , 'm'   ),
        ('speed'          , 'm_speed'         , lambda x: '{:.1f}'.format(x * 3.6) , 'km/h'),
        ('throttle'       , 'm_throttle'      , lambda x: '{:.3f}'.format(x)       , '-'   ),
        ('steer'          , 'm_steer'         , lambda x: '{:.3f}'.format(x)       , '-'   ),
        ('brake'          , 'm_brake'         , lambda x: '{:.3f}'.format(x)       , '-'   ),
        ('clutch'         , 'm_clutch'        , lambda x: '{:.3f}'.format(x)       , '-'   ),
        ('gear'           , 'm_gear'          , lambda x: '{:.0f}'.format(x)       , '-'   ),
        ('lap'            , 'm_lap'           , lambda x: '{:.0f}'.format(x)       , '-'   ),
        ('car position'   , 'm_car_position'  , lambda x: '{:.0f}'.format(x)       , '-'   )
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QGridLayout()

        self._value_labels = []

        for i, (label, fieldname, formatter, unit) in enumerate(CentralWidget.fields):

            key_label   = QtWidgets.QLabel(label)
            value_label = QtWidgets.QLabel("n/a")
            unit_label  = QtWidgets.QLabel(unit)

            layout.addWidget(key_label  , i, 0)
            layout.addWidget(value_label, i, 1)
            layout.addWidget(unit_label , i, 2)

            self._value_labels.append(value_label)

        self.setLayout(layout)

        app = QtWidgets.QApplication.instance()
        app.telemetry.connect(self.processTelemetry)

    def processTelemetry(self, telemetry):
        for i, (label, fieldname, formatter, unit) in enumerate(CentralWidget.fields):
            self._value_labels[i].setText(formatter(telemetry[0][fieldname]))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('F1-2017 Telemetry')
        widget = CentralWidget()
        self.setCentralWidget(widget)

class Application(QtWidgets.QApplication):

    telemetry = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        udpSocket = QtNetwork.QUdpSocket()
        udpSocket.bind(QtNetwork.QHostAddress.Any, 20777)

        udpSocket.readyRead.connect(self.readPendingDatagrams)

        mainWindow = MainWindow()
        mainWindow.show()

        self._udpSocket  = udpSocket
        self._mainWindow = mainWindow

    def readPendingDatagrams(self):
        while self._udpSocket.hasPendingDatagrams():
            datagram = self._udpSocket.receiveDatagram()

            telemetry = np.frombuffer(datagram.data(), dtype = F1_2017_UDPPacket)

            self.telemetry.emit(telemetry)

def main():
    app = Application(sys.argv)
    exitcode = app.exec()
    sys.exit(exitcode)

if __name__ == "__main__":
    main()

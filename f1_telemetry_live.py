 #! /usr/bin/env python3

import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtNetwork, QtGui

from f1_telemetry_dtype import F1_2017_UDPPacket

app = None

class CentralWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        label.setAlignment(QtCore.Qt.AlignCenter)
        font = label.font()
        font.setPointSize(480)
        label.setFont(font)

        layout.addWidget(label)
        self.setLayout(layout)

        self._label = label

        app = QtWidgets.QApplication.instance()
        app.f1Data.connect(self.updateAll)

    def updateAll(self, data):
        speed = data[0]['m_speed']
        self._label.setText("{:.1f}".format(3.6 * speed))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget = CentralWidget()
        self.setCentralWidget(widget)

class Application(QtWidgets.QApplication):

    f1Data = QtCore.pyqtSignal(np.ndarray)

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

            data = np.frombuffer(datagram.data(), dtype = F1_2017_UDPPacket)

            self.f1Data.emit(data)

def main():
    app = Application(sys.argv)
    exitcode = app.exec()
    sys.exit(exitcode)

if __name__ == "__main__":
    main()

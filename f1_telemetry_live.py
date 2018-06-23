 #! /usr/bin/env python3

import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtNetwork, QtGui

from f1_telemetry_dtype import F1_2017_UDPPacket, F1_2017_Drivers, F1_2017_Teams, F1_2017_TyreCompounds

app = None

class MyCarTelemetryModel(QtCore.QAbstractTableModel):

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
        self._values = [None for field in MyCarTelemetryModel.fields]

        app = QtWidgets.QApplication.instance()
        app.telemetryData.connect(self.processTelemetryData)

    def rowCount(self, parent):
        return len(MyCarTelemetryModel.fields)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        row = index.row()
        col = index.column()
        field = MyCarTelemetryModel.fields[row]
        if role == QtCore.Qt.DisplayRole:
            if col == 0:
                return field[0]
            elif col == 1:
                value = self._values[row]
                if value is None:
                    return "(not available)"
                formatter = field[2]
                return formatter(value)
            elif col == 2:
                return "[{}]".format(field[3])

        return QtCore.QVariant()

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                if section == 0:
                    return "name"
                elif section == 1:
                    return "value"
                elif section == 2:
                    return "unit"
        return QtCore.QVariant()

    def processTelemetryData(self, telemetry):
        for i, (label, fieldname, formatter, unit) in enumerate(MyCarTelemetryModel.fields):
            self._values[i] = telemetry[0][fieldname]

        topleft = self.createIndex(0, 1)
        bottomright = self.createIndex(len(MyCarTelemetryModel.fields) - 1, 1)
        self.dataChanged.emit(topleft, bottomright)


class AllCarsTelemetryModel(QtCore.QAbstractTableModel):

    fields = [
        ('last lap time'     , 'm_lastLapTime'       , lambda x: '{:.3f}'.format(x)       , 's' ),
        ('current lap time'  , 'm_currentLapTime'    , lambda x: '{:.3f}'.format(x)       , 's' ),
        ('best lap time'     , 'm_bestLapTime'       , lambda x: '{:.3f}'.format(x)       , 's' ),
        ('S1'                , 'm_sector1Time'       , lambda x: '{:.3f}'.format(x)       , 's' ),
        ('S2'                , 'm_sector2Time'       , lambda x: '{:.3f}'.format(x)       , 's' ),
        ('lap distance'      , 'm_lapDistance'       , lambda x: '{:.1f}'.format(x)       , 'm' ),
        ('driver'            , 'm_driverId'          , lambda x: F1_2017_Drivers[x]       , None),
        ('team'              , 'm_teamId'            , lambda x: F1_2017_Teams[x]         , None),
        ('position'          , 'm_carPosition'       , lambda x: 'P{:d}'.format(x)        , None),
        ('lap'               , 'm_currentLapNum'     , lambda x: 'L{:d}'.format(x)        , None),
        ('tyre compound'     , 'm_tyreCompound'      , lambda x: F1_2017_TyreCompounds[x] , None),
        ('in pits?'          , 'm_inPits'            , lambda x: '{:d}'.format(x)         , None),
        ('sector'            , 'm_sector'            , lambda x: 'S{:d}'.format(x + 1)    , None),
        ('lap invalid?'      , 'm_currentLapInvalid' , lambda x: '{:d}'.format(x)         , None),
        ('penalties'         , 'm_penalties'         , lambda x: '{:d}'.format(x)         , 's' )
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = [[None for field in AllCarsTelemetryModel.fields] for i in range(20)]

        app = QtWidgets.QApplication.instance()
        app.telemetryData.connect(self.processTelemetryData)

    def rowCount(self, parent):
        return 20

    def columnCount(self, parent):
        return len(AllCarsTelemetryModel.fields)

    def data(self, index, role):
        row = index.row()
        col = index.column()
        field = AllCarsTelemetryModel.fields[col]
        if role == QtCore.Qt.DisplayRole:
            value = self._values[row][col]
            if value is None:
                return "(not available)"
            formatter = field[2]
            return formatter(value)

        return QtCore.QVariant()

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                field = self.fields[section]
                fieldname = field[0]
                unit = field[3]
                return fieldname if unit is None else "{} [{}]".format(fieldname, unit)
                return self.fields[section][0]
        elif orientation == QtCore.Qt.Vertical:
            if role == QtCore.Qt.DisplayRole:
                return "{}".format(section)
        return QtCore.QVariant()

    def processTelemetryData(self, telemetry):
        for car in range(20):
            for i, (label, fieldname, formatter, unit) in enumerate(AllCarsTelemetryModel.fields):
                self._values[car][i] = telemetry[0]['m_car_data'][car][fieldname]

        # Sort by car position
        self._values.sort(key = lambda x: x[8])

        topleft = self.createIndex(0, 0)
        bottomright = self.createIndex(19, len(MyCarTelemetryModel.fields) - 1)
        self.dataChanged.emit(topleft, bottomright)


class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('F1-2017 Telemetry')

        myCarTelemetryModel = MyCarTelemetryModel() 
        myCarTelemetryWidget = QtWidgets.QTableView()
        myCarTelemetryWidget.setModel(myCarTelemetryModel)

        allCarsTelemetryModel = AllCarsTelemetryModel() 
        allCarsTelemetryWidget = QtWidgets.QTableView()
        allCarsTelemetryWidget.setModel(allCarsTelemetryModel)

        self.addTab(myCarTelemetryWidget, "My Car")
        self.addTab(allCarsTelemetryWidget, "All Cars")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('F1-2017 Telemetry')

        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)

class Application(QtWidgets.QApplication):

    telemetryData = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, port, *args, **kwargs):
        super().__init__(*args, **kwargs)

        udpSocket = QtNetwork.QUdpSocket()
        udpSocket.bind(QtNetwork.QHostAddress.Any, port)

        udpSocket.readyRead.connect(self.readPendingDatagrams)

        mainWindow = MainWindow()
        mainWindow.show()

        self._udpSocket  = udpSocket
        self._mainWindow = mainWindow

    def readPendingDatagrams(self):
        while self._udpSocket.hasPendingDatagrams():
            datagram = self._udpSocket.receiveDatagram()

            telemetry = np.frombuffer(datagram.data(), dtype = F1_2017_UDPPacket)

            self.telemetryData.emit(telemetry)

app = None

def main():
    global app
    app = Application(20777, sys.argv)
    exitcode = app.exec()
    sys.exit(exitcode)

if __name__ == "__main__":
    main()

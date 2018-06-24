 #! /usr/bin/env python3

import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, QtNetwork, QtGui

import f1_2017_defs as f1_2017

class MyCarTableModel(QtCore.QAbstractTableModel):

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
        self._values = [None for field in MyCarTableModel.fields]

        app = QtWidgets.QApplication.instance()
        app.telemetryReceived.connect(self.processTelemetry)

    def rowCount(self, parent):
        return len(MyCarTableModel.fields)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        row = index.row()
        col = index.column()
        field = MyCarTableModel.fields[row]
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

    def processTelemetry(self, telemetry):
        for i, (label, fieldname, formatter, unit) in enumerate(MyCarTableModel.fields):
            self._values[i] = telemetry[fieldname]

        topleft = self.createIndex(0, 1)
        bottomright = self.createIndex(len(MyCarTableModel.fields) - 1, 1)
        self.dataChanged.emit(topleft, bottomright)


class AllCarsTableModel(QtCore.QAbstractTableModel):

    def format_time(t):
        return "n/a" if t == 0.0 else "{:.3f}".format(t)

    fields = [
        ('last lap time'     , 'm_lastLapTime'       , format_time                            , 's' ),
        ('current lap time'  , 'm_currentLapTime'    , format_time                            , 's' ),
        ('best lap time'     , 'm_bestLapTime'       , format_time                            , 's' ),
        ('S1'                , 'm_sector1Time'       , format_time                            , 's' ),
        ('S2'                , 'm_sector2Time'       , format_time                            , 's' ),
        ('lap distance'      , 'm_lapDistance'       , lambda x: '{:.1f}'.format(x)           , 'm' ),
        ('driver'            , 'm_driverId'          , lambda x: f1_2017.Drivers[x].shortname , None),
        ('team'              , 'm_teamId'            , lambda x: f1_2017.Teams[x].name        , None),
        ('position'          , 'm_carPosition'       , lambda x: 'P{:d}'.format(x)            , None),
        ('lap'               , 'm_currentLapNum'     , lambda x: 'L{:d}'.format(x)            , None),
        ('tyre compound'     , 'm_tyreCompound'      , lambda x: f1_2017.TyreCompounds[x]     , None),
        ('in pits?'          , 'm_inPits'            , lambda x: '{:d}'.format(x)             , None),
        ('sector'            , 'm_sector'            , lambda x: 'S{:d}'.format(x + 1)        , None),
        ('lap invalid?'      , 'm_currentLapInvalid' , lambda x: '{:d}'.format(x)             , None),
        ('penalties'         , 'm_penalties'         , lambda x: '{:d}'.format(x)             , 's' )
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = [[None for field in AllCarsTableModel.fields] for i in range(f1_2017.NumberOfCars)]

        app = QtWidgets.QApplication.instance()
        app.telemetryReceived.connect(self.processTelemetry)

    def rowCount(self, parent):
        return f1_2017.NumberOfCars

    def columnCount(self, parent):
        return len(AllCarsTableModel.fields)

    def data(self, index, role):
        row = index.row()
        col = index.column()
        field = AllCarsTableModel.fields[col]
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

        return QtCore.QVariant()

    def processTelemetry(self, telemetry):

        for car in range(f1_2017.NumberOfCars):
            for i, (label, fieldname, formatter, unit) in enumerate(AllCarsTableModel.fields):
                self._values[car][i] = telemetry['m_car_data'][car][fieldname]

        # Sort by car position
        self._values.sort(key = lambda x: x[8])

        topleft = self.createIndex(0, 0)
        bottomright = self.createIndex(19, len(MyCarTableModel.fields) - 1)
        self.dataChanged.emit(topleft, bottomright)

class CircuitMapScene(QtWidgets.QGraphicsScene):

    MAP_SIZE = 2400
    CAR_SIZE = 50.0
    DRIVER_SIZE = 20.0

    PEN_WIDTH    = (CAR_SIZE - DRIVER_SIZE) / 2
    ELLIPSE_SIZE = (CAR_SIZE + DRIVER_SIZE) / 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_track_number = None
        self._pixmap = QtGui.QPixmap(CircuitMapScene.MAP_SIZE, CircuitMapScene.MAP_SIZE)
        self.resetMap()
        self._background = self.addPixmap(self._pixmap)
        self._background.setOffset(-CircuitMapScene.MAP_SIZE / 2, -CircuitMapScene.MAP_SIZE / 2)
        self._drivers = {}
        for driver_id in f1_2017.Drivers:
            driver_graphic = self.addEllipse(-CircuitMapScene.ELLIPSE_SIZE/2, -CircuitMapScene.ELLIPSE_SIZE/2,
                CircuitMapScene.ELLIPSE_SIZE, CircuitMapScene.ELLIPSE_SIZE)
            self._drivers[driver_id] = driver_graphic

        app = QtWidgets.QApplication.instance()
        app.telemetryReceived.connect(self.processTelemetry)

    def resetMap(self):
        self._pixmap.fill(QtGui.QColor('#eeeeee'))

    def processTelemetry(self, telemetry):

        track_number = telemetry['m_track_number']
        if track_number != self._current_track_number:
            self._current_track_number = track_number
            self.resetMap()

        painter = QtGui.QPainter(self._pixmap)
        painter.setPen(QtGui.QColor("#cccccc"))
        cars = telemetry['m_car_data']
        for (car_index, car) in enumerate(cars):
            driver_id = car['m_driverId']
            team_id = car['m_teamId']
            team = f1_2017.Teams[team_id]
            driver = f1_2017.Drivers[driver_id]
            driver_graphic = self._drivers[driver_id]
            wpos = car['m_worldPosition']
            (x, y, z) = wpos

            pen_width = CircuitMapScene.PEN_WIDTH
            ellipse_size = CircuitMapScene.ELLIPSE_SIZE

            if car_index == telemetry['m_player_car_index']:
                pen_width *= 2
                ellipse_size *= 2

            pen = QtGui.QPen(QtGui.QColor(team.color))
            pen.setWidth(pen_width)
            brush = QtGui.QBrush(QtGui.QColor(driver.color))

            driver_graphic.setRect(x - ellipse_size/2, z - ellipse_size/2, ellipse_size, ellipse_size)
            driver_graphic.setPen(pen)
            driver_graphic.setBrush(brush)

            # Update circuit map in pixmap.
            painter.drawEllipse(x + CircuitMapScene.MAP_SIZE/2, z + CircuitMapScene.MAP_SIZE/2, 20.0, 20.0)

        painter.end()
        self._background.setPixmap(self._pixmap)


class CentralWidget(QtWidgets.QTabWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('F1-2017 Telemetry')

        myCarTableModel = MyCarTableModel() 
        myCarTableWidget = QtWidgets.QTableView()
        myCarTableWidget.setModel(myCarTableModel)

        allCarsTableModel = AllCarsTableModel() 
        allCarsTableWidget = QtWidgets.QTableView()
        allCarsTableWidget.setModel(allCarsTableModel)

        circuitMapScene  = CircuitMapScene()
        circuitMapWidget = QtWidgets.QGraphicsView(circuitMapScene)

        circuitMapWidget.fitInView(0.0, 0.0, 2400.0, 2400.0, QtCore.Qt.KeepAspectRatio)

        self.addTab(myCarTableWidget, "My Car")
        self.addTab(allCarsTableWidget, "All Cars")
        self.addTab(circuitMapWidget, "Circuit Map")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('F1-2017 Telemetry')

        centralWidget = CentralWidget()
        self.setCentralWidget(centralWidget)


class Application(QtWidgets.QApplication):

    telemetryReceived = QtCore.pyqtSignal(np.void)

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

            telemetry = np.frombuffer(datagram.data(), dtype = f1_2017.UDPPacket)

            telemetry = telemetry[0] # Convert from 1-element from numpy.ndarray to numpy.void

            self.telemetryReceived.emit(telemetry)


app = None # Prevents problems at shutdown.

def main():

    global app # Prevents problems at shutdown.

    app = Application(20777, sys.argv)
    exitcode = app.exec()
    sys.exit(exitcode)


if __name__ == "__main__":
    main()

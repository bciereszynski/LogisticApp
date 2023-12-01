import uuid

from PyQt5.QtCore import Qt

from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QAction, QFileDialog, QMainWindow, QWidget, \
    QTabWidget, QVBoxLayout, QLabel

from src.calc.algorithmTOP import runAlgorithm
from src.common.Courier import Courier
from src.common.Point import Point
from src.data.repositories.CourierRepository import CouriersRepository
from src.data.FileReader import FileReader
from src.data.ItemsList import ItemsList
from src.data.repositories.PointsRepository import PointsRepository
from src.mail.sender import send_mail
from src.ui.Editors import AddIntegerEditor
from src.ui.dialogs.ConfigDialog import ConfigWindow
from src.ui.dialogs.CourierDialog import CourierDialog
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget
from src.ui.dialogs.PointDialog import PointDialog


class MainWindow(QMainWindow):

    def __init__(self, config):
        super().__init__()
        self.setWindowTitle('Logistic App')
        self.window_width, self.window_height = 1200, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        self.config = config

        pointsRepository = PointsRepository()
        self.pointsList = ItemsList(pointsRepository, Point)
        couriersRepository = CouriersRepository()
        self.couriersList = ItemsList(couriersRepository, Courier)

        lay = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(lay)

        self.setCentralWidget(widget)
        self.createActions()
        self.createMenus()

        self.mapWidget = MapWidget(self.pointsList, self.config)

        self.pointsMenu = ItemsMenu(self.pointsList, PointDialog())
        self.pointsList.fetch()

        self.couriersMenu = ItemsMenu(self.couriersList, CourierDialog())
        self.couriersList.fetch()
        self.couriersMenu.itemSelectionChanged().connect(self.showCourierMap)

        vLay = QVBoxLayout()
        toolbarLay = QHBoxLayout()
        toolbarLay.setAlignment(Qt.AlignRight)

        tLabel, self.tmaxSpin = AddIntegerEditor(toolbarLay, "t_max (m)")
        self.tmaxSpin.setMaximum(2147483647)
        self.tmaxSpin.setValue(10000)
        self.tmaxSpin.setMinimumWidth(50)
        valueLabel = QLabel("Value:")
        self.valueDisplayLabel = QLabel("...")
        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        generateBtn.clicked.connect(self.generate)
        toolbarLay.addWidget(valueLabel)
        toolbarLay.addWidget(self.valueDisplayLabel)
        toolbarLay.addWidget(generateBtn)

        vLay.addLayout(toolbarLay)

        tabsWidget = QTabWidget()
        tabsWidget.addTab(self.pointsMenu, "Points")
        tabsWidget.addTab(self.couriersMenu, "Couriers")

        vLay.addWidget(tabsWidget)
        lay.addWidget(self.mapWidget, stretch=1)
        lay.addLayout(vLay, stretch=0)


    def showCourierMap(self, selectedItem, unselectedItem):
        index = self.couriersMenu.itemsWidget.row(selectedItem)
        self.mapWidget.setMap(index)

    def createActions(self):
        act = QAction("Load points from file", self)
        act.triggered.connect(self.loadPointsFromFile)
        self.loadPointsFromFileAct = act

        act = QAction("Edit", self)
        act.triggered.connect(self.showConfigEditor)
        self.editConfig = act

        act = QAction("Send to currnent", self)
        act.triggered.connect(self.sendToCurrent)
        self.sendCurrentAct = act

        act = QAction("Send to all", self)
        self.sendAllAct = act

    def createMenus(self):
        dataMenu = self.menuBar().addMenu("Data")
        dataMenu.addAction(self.loadPointsFromFileAct)

        configMenu = self.menuBar().addMenu("Configuration")
        configMenu.addAction(self.editConfig)

        mailMenu = self.menuBar().addMenu("Mail")
        mailMenu.addAction(self.sendCurrentAct)
        mailMenu.addAction(self.sendAllAct)

    def loadPointsFromFile(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        try:
            points = FileReader.read_points(fileName[0])
        except Exception:
            self.__showErrorMsg("Error during file import")
            return

        for point in points:
            point.id = uuid.uuid3(point.id, point.name)
            self.pointsList.append(point)

    def showConfigEditor(self):
        configEditor = ConfigWindow(self.config)
        configEditor.exec()

    def sendToCurrent(self):
        index = self.couriersMenu.selectedIndex().row()
        if index is None:
            return
        try:
            with open("map.html", "w") as f:
                f.write(self.mapWidget.getHtml())
        except Exception:
            self.__showErrorMsg("Error during file write")
            return
        send_mail(self.couriersList.getItem(index).email, "Your route", " ",
                  self.config.mailLogin, self.config.mailPassword, "map.html")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Mail send to " + self.couriersList.getItem(index).email)
        msg.setWindowTitle("Success!")
        msg.exec_()

    def generate(self):
        points = self.pointsList.getItems()
        matrixApi = MatrixAPI(self.config)
        try:
            distances_map = matrixApi.get_result(points)
        except Exception as ex:
            self.__showErrorMsg(str(ex))
            return

        couriers = self.couriersList.getItems()
        t_max = self.tmaxSpin.value()

        try:
            routes = runAlgorithm(points, distances_map, t_max, couriers)
        except Exception as ex:
            self.__showErrorMsg(str(ex))
            return
        value = 0
        for r in routes:
            value += r.get_value()
        self.valueDisplayLabel.setText(str(value))
        self.mapWidget.routes = routes
        self.mapWidget.update()

    @staticmethod
    def __showErrorMsg(msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText("Error")
        msgBox.setInformativeText(msg)
        msgBox.setWindowTitle("Error")
        msgBox.exec_()
        return

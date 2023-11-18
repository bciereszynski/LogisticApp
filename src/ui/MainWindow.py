import random
import uuid

from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QAction, QFileDialog, QMainWindow, QWidget, \
    QTabWidget, QVBoxLayout

from src.common.Courier import Courier
from src.common.Point import Point
from src.common.Route import Route
from src.data.CourierRepository import CouriersRepository
from src.data.FileReader import FileReader
from src.data.ItemsList import ItemsList
from src.data.PointsRepository import PointsRepository
from src.ui.ConfigWindow import ConfigWindow
from src.ui.CourierDialog import CourierDialog
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget
from src.ui.PointDialog import PointDialog


class MainWindow(QMainWindow):

    def generate(self):
        points = self.pointsList.getItems()
        matrixApi = MatrixAPI(self.config)
        try:
            distances_map = matrixApi.get_distances_map(points)
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(ex))
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        couriers = self.couriersList.getItems()
        t_max = 10230
        central: Point = points[0]
        routes = []

        for i in range(len(couriers)):
            points_to_delegate = points.copy()
            route = Route(central)
            route.courier = couriers[i]
            routes.append(route)
            points_to_delegate.remove(central)
            last = central
            cost = 0
            while len(points_to_delegate) > 0:
                rand_point = points_to_delegate[random.randint(0, len(points_to_delegate) - 1)]
                if cost + distances_map[(rand_point, last)] + distances_map[(rand_point, central)] < t_max:
                    route.add(rand_point)
                    cost = cost + rand_point.calc_line_distance(last)
                    last = rand_point
                points_to_delegate.remove(rand_point)

        for r in routes:
            r.optimize()

        self.mapWidget.routes = routes
        self.mapWidget.update()

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

        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        generateBtn.clicked.connect(self.generate)

        tabsWidget = QTabWidget()
        tabsWidget.addTab(self.pointsMenu, "Points")
        tabsWidget.addTab(self.couriersMenu, "Couriers")

        lay.addWidget(self.mapWidget, stretch=1)
        lay.addWidget(tabsWidget, stretch=0)

        btnLay = QVBoxLayout()
        btnLay.addWidget(generateBtn)

        lay.addLayout(btnLay)

    def createActions(self):
        act = QAction("Load points from file", self)
        act.triggered.connect(self.loadPointsFromFile)
        self.loadPointsFromFileAct = act

        act = QAction("Edit", self)
        act.triggered.connect(self.showConfigEditor)
        self.editConfig = act

    def createMenus(self):
        dataMenu = self.menuBar().addMenu("Data")
        dataMenu.addAction(self.loadPointsFromFileAct)

        configMenu = self.menuBar().addMenu("Configuration")
        configMenu.addAction(self.editConfig)

    def loadPointsFromFile(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        try:
            points = FileReader.read_points(fileName[0])
        except Exception:
            messageBox = QMessageBox()
            messageBox.setText("Error occurred")
            messageBox.setInformativeText("during file import")
            messageBox.setIcon(QMessageBox.Warning)
            messageBox.setWindowTitle("Error")
            messageBox.exec()
            return

        for point in points:
            point.id = uuid.uuid3(point.id, point.name)
            self.pointsList.append(point)

    def showConfigEditor(self):
        configEditor = ConfigWindow(self.config)
        configEditor.exec()

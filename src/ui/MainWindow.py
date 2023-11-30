import random
import uuid

from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QAction, QFileDialog, QMainWindow, QWidget, \
    QTabWidget, QVBoxLayout

from src.common.Courier import Courier
from src.common.Point import Point
from src.common.Route import Route
from src.data.repositories.CourierRepository import CouriersRepository
from src.data.FileReader import FileReader
from src.data.ItemsList import ItemsList
from src.data.repositories.PointsRepository import PointsRepository
from src.ui.dialogs.ConfigDialog import ConfigWindow
from src.ui.dialogs.CourierDialog import CourierDialog
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget
from src.ui.dialogs.PointDialog import PointDialog


class MainWindow(QMainWindow):

    def construct(self, t_max, couriers, points, distances):
        routes = []
        central: Point = points[0]

        points = points.copy()
        points.remove(central)
        points_to_delegate = []
        delegated_points = []

        # filter out all location that cannot be reached
        for p in points:
            if (distances[(p.get_coordinates_str(), central.get_coordinates_str())] +
                    distances[(central.get_coordinates_str(), p.get_coordinates_str())] <= t_max):
                points_to_delegate.append(p)

        if len(points_to_delegate) < len(couriers):
            raise Exception("Unreal conditions")

        # create starting routes
        # find the furthest points
        dest_point_distance = []
        for dest_point in points_to_delegate:
            dest_point_distance.append(
                (dest_point, distances[(central.get_coordinates_str(), dest_point.get_coordinates_str())]))
        dest_point_distance.sort(reverse=True, key=lambda item: item[1])

        # create routes containing of one furthest point
        for i in range(len(couriers)):
            route = Route(central, distances)
            route.courier = couriers[i]
            routes.append(route)

            dest_point = dest_point_distance[i][0]
            route.add(dest_point)
            points_to_delegate.remove(dest_point)
            delegated_points.append((dest_point, route))

        # insert points to routes using the cheapest cost method
        for point in points_to_delegate.copy():
            min_change = float('inf')
            index = None
            selected_route = None
            for route in routes:
                change, i = route.check_insert_change(point)
                if min_change > change and change + route.get_length() <= t_max:
                    min_change = change
                    index = i
                    selected_route = route
                else:
                    print(route.get_length())
                    print(point.name)
                    print(str(change) + '\n')
            if index is not None:
                selected_route.insert(point, index)
                points_to_delegate.remove(point)

        # #
        # random method
        #     while len(points_to_delegate) > 0:
        #         rand_point = points_to_delegate[random.randint(0, len(points_to_delegate) - 1)]
        #         if cost + distances[(rand_point, last)] + distances[(rand_point, central)] < t_max:
        #             route.add(rand_point)
        #             cost = cost + rand_point.calc_line_distance(last)
        #             last = rand_point
        #         points_to_delegate.remove(rand_point)
        return routes

    def generate(self):
        points = self.pointsList.getItems()
        matrixApi = MatrixAPI(self.config)
        try:
            distances_map = matrixApi.get_result(points)
        except Exception as ex:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText(str(ex))
            msg.setWindowTitle("Error")
            msg.exec_()
            return

        couriers = self.couriersList.getItems()
        t_max = 15230
        routes = self.construct(t_max,couriers,points, distances_map)

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
        self.couriersMenu.itemSelectionChanged().connect(self.showCourierMap)

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

import random
import uuid

from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QAction, QFileDialog, QMainWindow, QWidget

from src.common.Point import Point
from src.common.Route import Route
from src.data.FileReader import FileReader
from src.data.ItemsList import ItemsList
from src.data.PointsRepository import PointsRepository
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget
from src.ui.PointDialog import PointDialog


class MainWindow(QMainWindow):

    def generate(self):
        points = self.pointsList.getItems()
        matrixApi = MatrixAPI()
        distances_map = matrixApi.get_distances_map(points)
        # try:
        #     distances_map = matrixApi.get_distances_map(self.points)
        # # except:
        # #     msg = QMessageBox()
        # #     msg.setIcon(QMessageBox.Critical)
        # #     msg.setText("Error")
        # #     msg.setInformativeText('Api error')
        # #     msg.setWindowTitle("Error")
        # #     msg.exec_()
        # #     return

        pop_size = 5
        t_max = 10230
        central: Point = points[0]
        routes = []

        for i in range(pop_size):
            points_to_delegate = points.copy()
            routes.append(Route(central))
            points_to_delegate.remove(central)
            last = central
            cost = 0
            while len(points_to_delegate) > 0:
                rand_point = points_to_delegate[random.randint(0, len(points_to_delegate) - 1)]
                if cost + distances_map[(rand_point, last)] + distances_map[(rand_point, central)] < t_max:
                    routes[i].add(rand_point)
                    cost = cost + rand_point.calc_line_distance(last)
                    last = rand_point
                points_to_delegate.remove(rand_point)

        for r in routes:
            r.optimize()

        self.mapWidget.routes = routes
        self.mapWidget.update()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Logistic App')
        self.window_width, self.window_height = 1200, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        pointsRepository = PointsRepository()
        self.pointsList = ItemsList(pointsRepository, Point)

        lay = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)
        self.createActions()
        self.createMenu()

        self.mapWidget = MapWidget(self.pointsList)
        self.pointsMenu = ItemsMenu(self.pointsList, PointDialog())
        self.pointsList.fetch()

        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        generateBtn.clicked.connect(self.generate)

        lay.addWidget(self.mapWidget, stretch=1)
        lay.addWidget(self.pointsMenu, stretch=0)
        lay.addWidget(generateBtn)



    def createActions(self):
        act = QAction("Load points from file", self)
        act.triggered.connect(self.loadPointsFromFile)
        self.loadPointsFromFileAct = act

    def createMenu(self):
        dataMenu = self.menuBar().addMenu("Data")
        dataMenu.addAction(self.loadPointsFromFileAct)

    def loadPointsFromFile(self):
        fileName = QFileDialog.getOpenFileName(self)
        if not fileName[0]:
            return

        try:
            points = FileReader.read_points(fileName[0])
        except:
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

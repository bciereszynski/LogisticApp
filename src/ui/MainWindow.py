import uuid

from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QPushButton, QMessageBox, QHBoxLayout, QAction, QFileDialog, QMainWindow, QWidget

from src.calc.main import generateRoutes
from src.common.Point import Point
from src.data.FileReader import FileReader
from src.data.ItemsList import ItemsList
from src.data.PointsRepository import PointsRepository
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget
from src.ui.PointDialog import PointDialog


class MainWindow(QMainWindow):

    def generate_distances(self):
        matrixApi = MatrixAPI()
        try:
            distances_map = matrixApi.get_distances_map(self.points)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Api error')
            msg.setWindowTitle("Error")
            msg.exec_()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Logistic App')
        self.window_width, self.window_height = 1200, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        self.pointsRepository = PointsRepository()
        pointsList = ItemsList(self.pointsRepository, Point)

        lay = QHBoxLayout()
        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)
        self.createActions()
        self.createMenu()

        self.mapWidget = MapWidget(pointsList)
        self.pointsMenu = ItemsMenu(pointsList, PointDialog())
        pointsList.fetch()


        updateBtn = QPushButton()
        updateBtn.setText("Update")
        updateBtn.clicked.connect(self.mapWidget.update)

        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        # generateBtn.clicked.connect(self.generate_distances)

        lay.addWidget(self.mapWidget, stretch=1)
        lay.addWidget(self.pointsMenu, stretch=0)
        lay.addWidget(updateBtn)
        # lay.addWidget(generateBtn)

        #routes = generateRoutes([], 15, 15.23)

        #mapWidget.routes = routes


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
            self.pointsRepository.Add(point)

        self.pointsMenu.updateItems()

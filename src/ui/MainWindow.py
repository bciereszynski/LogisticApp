from src.api.MatrixAPI import MatrixAPI

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout

from src.calc.main import generateRoutes
from src.data.FileReader import FileReader
from src.ui.ItemsMenu import ItemsMenu
from src.ui.MapWidget import MapWidget

class MainWindow(QWidget):

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

        lay = QHBoxLayout()
        self.setLayout(lay)

        points = FileReader.read_points('src/data/data.txt')
        mapWidget = MapWidget(points)
        lay.addWidget(mapWidget, stretch=1)
        pointsMenu = ItemsMenu(None)
        lay.addWidget(pointsMenu, stretch=0)

        updateBtn = QPushButton()
        updateBtn.setText("Update")
        updateBtn.clicked.connect(mapWidget.update)

        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        # generateBtn.clicked.connect(self.generate_distances)

        lay.addWidget(updateBtn)
        # lay.addWidget(generateBtn)

        routes = generateRoutes(points, 15, 15.23)

        mapWidget.routes = routes

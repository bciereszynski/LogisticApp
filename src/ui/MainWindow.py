from src.common.Point import Point
from src.api.DirectionsAPI import DirectionsAPI
from src.api.MatrixAPI import MatrixAPI
import io
import pandas as pd
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
from src.data.FileReader import FileReader


class MainWindow(QWidget):
    def create_map(self, points):
        m = folium.Map()
        m.add_child(folium.LatLngPopup())
        df = pd.DataFrame([(point.get_longitude(),point.get_latitude()) for point in points])
        # add markers
        for point in points:
            folium.Marker((point.get_longitude(),point.get_latitude())).add_to(m)
        # create optimal zoom
        sw = df.min().values.tolist()
        sw = [sw[0] - 0.0005, sw[1] - 0.0005]
        ne = df.max().values.tolist()
        ne = [ne[0] + 0.0005, ne[1] + 0.0005]
        m.fit_bounds([sw, ne])
        return m

    def update_map(self):
        dirApi = DirectionsAPI()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('This action may take a while')
        msg.setWindowTitle("Wait...")
        msg.exec_()

        for i in range(len(self.points) - 1):
            point1 = self.points[i]
            point2 = self.points[i+1]
            coordinates = dirApi.get_path_coordinates(point1, point2)
            folium.PolyLine(coordinates, color="red", weight=5,
                            opacity=1).add_to(self.m)

        # save map data to data object
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

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
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1200, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        updateBtn = QPushButton()
        updateBtn.setText("Update")
        updateBtn.move(64, 32)
        updateBtn.clicked.connect(self.update_map)

        generateBtn = QPushButton()
        generateBtn.setText("Generate")
        generateBtn.move(64, 32)
        generateBtn.clicked.connect(self.generate_distances)

        layout.addWidget(updateBtn)
        layout.addWidget(generateBtn)

        self.points = FileReader.read_points('src/data/data.txt')
        self.m = self.create_map(self.points)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)
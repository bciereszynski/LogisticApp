from src.common.Point import Point
from src.api.DirectionsAPI import DirectionsAPI
import io
import pandas as pd
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine

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

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1200, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        button1 = QPushButton()
        button1.setText("Generate")
        button1.move(64, 32)
        button1.clicked.connect(self.update_map)

        layout.addWidget(button1)

        self.points = [Point(53.13013312030104, 23.159393296340824), Point(53.1060760891934, 23.185881011562742),
                       Point(53.105700348436585, 23.1489064504242)]
        self.m = self.create_map(self.points)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)
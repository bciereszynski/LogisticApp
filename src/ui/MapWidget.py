import io

import folium
import pandas as pd

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from src.api.DirectionsAPI import DirectionsAPI
from AppConfig import AppConfig


class MapWidget(QWidget):
    def __init__(self, pointsList, config: AppConfig):
        super().__init__()
        self.config = config
        lay = QVBoxLayout()
        self.setLayout(lay)

        self.pointsList = pointsList
        self.routes = None
        self.map = None

        self.pointsList.listChanged.connect(self.fetchPoints)

        self.webView = QWebEngineView()
        lay.addWidget(self.webView)

        self.__create(self.pointsList.getItems())

    def fetchPoints(self):
        points = self.pointsList.getItems()
        self.__create(points)

    def drawRoute(self, route):
        dirApi = DirectionsAPI(self.config)

        for i in range(len(route.points) - 1):
            point1 = route.points[i]
            point2 = route.points[i + 1]
            coordinates = dirApi.get_path_coordinates(point1, point2)
            folium.PolyLine(coordinates, color=route.courier.color, weight=6, #random.randint(1, 9),
                            opacity=1).add_to(self.map)

        # save map data to data object
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def update(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('This action may take a while')
        msg.setWindowTitle("Wait...")
        msg.exec_()

        for r in self.routes:
            self.drawRoute(r)

    def __create(self, points):
        self.map = folium.Map()
        self.map.add_child(folium.LatLngPopup())

        for point in points:
            folium.Marker((point.get_longitude(), point.get_latitude())).add_to(self.map)

        self.__scale(points)

        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

    def __scale(self, points):
        df = pd.DataFrame([(float(point.get_longitude()), float(point.get_latitude())) for point in points])
        sw = df.min().values.tolist()
        if len(sw) > 0:
            sw = [sw[0] - 0.0005, sw[1] - 0.0005]
        ne = df.max().values.tolist()
        if len(ne) > 0:
            ne = [ne[0] + 0.0005, ne[1] + 0.0005]

        self.map.fit_bounds([sw, ne])

import io

import folium
import pandas as pd

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from src.api.DirectionsAPI import DirectionsAPI
from src.AppConfig import AppConfig


class MapWidget(QWidget):
    def __init__(self, pointsList, config: AppConfig):
        super().__init__()
        self.config = config

        lay = QVBoxLayout()
        self.setLayout(lay)

        self.webView = QWebEngineView()
        lay.addWidget(self.webView)

        self.pointsList = pointsList
        self.routes = None
        self.map = None

        self.pointsList.listChanged.connect(self.fetchPoints)

        self.createMap(self.pointsList.getItems())

    def setMap(self, route):
        self.createMap(route.points)
        self.drawRoute(route)

    def fetchPoints(self):
        points = self.pointsList.getItems()
        self.createMap(points)

    def drawRoute(self, route):
        dirApi = DirectionsAPI(self.config)

        for i in range(len(route.points) - 1):
            requestPoints = (route.points[i], route.points[i + 1])
            coordinates = dirApi.get_result(requestPoints)
            folium.PolyLine(coordinates, color=route.courier.color, weight=6,  # random.randint(1, 9),
                            opacity=1).add_to(self.map)

        requestPoints = (route.points[-1], route.points[0])
        coordinates = dirApi.get_result(requestPoints)
        folium.PolyLine(coordinates, color=route.courier.color, weight=6,  # random.randint(1, 9),
                        opacity=1).add_to(self.map)

        # save map data to data object
        self.webView.setHtml(self.getHtml())

    def getHtml(self):
        assert self.map is not None
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        return data.getvalue().decode()

    def update(self):
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setText('This action may take a while')
        # msg.setWindowTitle("Wait...")
        # msg.exec_()

        self.createMap(self.pointsList.getItems())

        for r in self.routes:
            self.drawRoute(r)

    def addMarker(self, point):
        popup = folium.Popup(folium.Html(
            """
            <b>Name: </b> {} </br>
            <b>Value: </b> {}
            """.format(point.name, point.get_value()), script=True
        ))
        if point.isCentral:
            icon = folium.Icon(color="red", icon="home")
        else:
            icon = None
        folium.Marker((point.get_longitude(), point.get_latitude()), popup=popup, icon=icon).add_to(self.map)

    def createMap(self, points):
        self.map = folium.Map(doubleClickZoom=False)
        self.map.add_child(folium.LatLngPopup())

        for point in points:
            self.addMarker(point)

        self.__scale(points)
        self.__setMap(self.map)

    def __scale(self, points):
        df = pd.DataFrame([(float(point.get_longitude()), float(point.get_latitude())) for point in points])
        sw = df.min().values.tolist()
        if len(sw) > 0:
            sw = [sw[0] - 0.0005, sw[1] - 0.0005]
        ne = df.max().values.tolist()
        if len(ne) > 0:
            ne = [ne[0] + 0.0005, ne[1] + 0.0005]

        self.map.fit_bounds([sw, ne])

    def __setMap(self, m):
        data = io.BytesIO()
        m.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())

import io
import folium
import pandas as pd

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from src.api.DirectionsAPI import DirectionsAPI


class MapWidget(QWidget):
    def __init__(self, points):
        super().__init__()
        lay = QVBoxLayout()
        self.setLayout(lay)

        self.points = points

        self.m = None
        self.__create(self.points)

        data = io.BytesIO()
        self.m.save(data, close_file=False)
        print(data.getvalue())
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        lay.addWidget(self.webView)

    def update(self):
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

    def __create(self, points):
        self.m = folium.Map()
        self.m.add_child(folium.LatLngPopup())

        # add markers
        for point in points:
            folium.Marker((point.get_longitude(), point.get_latitude())).add_to(self.m)

        # create optimal zoom
        df = pd.DataFrame([(point.get_longitude(), point.get_latitude()) for point in points])
        sw = df.min().values.tolist()
        sw = [sw[0] - 0.0005, sw[1] - 0.0005]
        ne = df.max().values.tolist()
        ne = [ne[0] + 0.0005, ne[1] + 0.0005]

        self.m.fit_bounds([sw, ne])

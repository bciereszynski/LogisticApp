import sys
import requests
import io
import pandas as pd
import folium
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine

"""
Folium in PyQt5
"""


class MainWindow(QWidget):

    def create_map(self, lat_lons):
        m = folium.Map()
        m.add_child(folium.LatLngPopup())
        df = pd.DataFrame(lat_lons)
        # add markers for the places we visit
        for point in lat_lons:
            folium.Marker(point).add_to(m)
        # create optimal zoom
        sw = df.min().values.tolist()
        sw = [sw[0] - 0.0005, sw[1] - 0.0005]
        ne = df.max().values.tolist()
        ne = [ne[0] + 0.0005, ne[1] + 0.0005]
        m.fit_bounds([sw, ne])
        return m

    def insert_paths(self, map, responses):
        for response in responses:
            mls = response.json()['route']['geometry']['coordinates']
            points = [(i[0], i[1]) for i in mls]
            # add the lines
            folium.PolyLine(points, color="red", weight=5,
                            opacity=1).add_to(map)

    def get_directions_response(self, lat1, long1, lat2, long2, mode='drive'):
        url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        headers = {
            "X-RapidAPI-Key": "6daf7a1653msh163f00b78136335p13cdfajsn22dd609d0a86",
            "X-RapidAPI-Host": "trueway-directions2.p.rapidapi.com"
        }
        querystring = {
            "stops": f"{str(lat1)},{str(long1)};{str(lat2)},{str(long2)}"}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return response

    def gen_map(self):
        lat_lons = self.lat_lons
        responses = []
        for n in range(len(lat_lons) - 1):
            lat1, lon1, lat2, lon2 = lat_lons[n][0], lat_lons[n][1], lat_lons[n +
                                                                              1][0], lat_lons[n + 1][1]
            response = self.get_directions_response(
                lat1, lon1, lat2, lon2)

            print(response.json()["route"]["distance"])

            responses.append(response)

        self.insert_paths(self.m, responses)

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
        button1.setText("Button")
        button1.move(64, 32)
        button1.clicked.connect(self.gen_map)

        layout.addWidget(button1)

        self.lat_lons = [[53.13013312030104, 23.159393296340824], [53.1060760891934, 23.185881011562742],
                         [53.105700348436585, 23.1489064504242]]
        self.m = self.create_map(self.lat_lons)
        data = io.BytesIO()
        self.m.save(data, close_file=False)
        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    window = MainWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget


class PointsMenu(QWidget):
    def __init__(self, points):
        super().__init__()
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.pointsList = QListWidget()
        self.pointsNames = [str(p) for p in points]
        self.pointsList.addItems(self.pointsNames)
        self.lay.addWidget(self.pointsList)

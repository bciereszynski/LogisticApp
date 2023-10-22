from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QWidget, QPushButton


class PointsMenu(QWidget):
    def __init__(self, points):
        super().__init__()
        self.lay = QVBoxLayout()
        self.setLayout(self.lay)

        self.pointsList = QListWidget()
        self.pointsNames = [str(p) for p in points]
        self.pointsList.addItems(self.pointsNames)
        self.lay.addWidget(self.pointsList)

        self.addBtn = QPushButton()
        self.addBtn.setText("Add")
        #self.addBtn.clicked.connect()

        self.deleteBtn = QPushButton()
        self.deleteBtn.setText("Delete")
        # self.deleteBtn.clicked.connect(self.generate_distances)

        self.lay.addWidget(self.addBtn)
        self.lay.addWidget(self.deleteBtn)

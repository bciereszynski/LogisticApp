from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QLabel, QDoubleSpinBox, QLineEdit, QSpinBox, QPushButton, QColorDialog, QHBoxLayout


def AddDecimalEditor(layout, name):
    label = QLabel(name)
    spin = QDoubleSpinBox()
    spin.setDecimals(15)

    layout.addWidget(label)
    layout.addWidget(spin)

    return label, spin


def AddStringEditor(layout, name):
    label = QLabel(name)
    line = QLineEdit()

    layout.addWidget(label)
    layout.addWidget(line)

    return label, line


def AddPasswordEditor(layout, name):
    innerLay = QHBoxLayout()
    label = QLabel(name)
    line = QLineEdit()
    btn = QPushButton("*")
    btn.setFixedSize(20, 20)

    def showPasswordCommand():
        if line.echoMode() == QLineEdit.Password:
            line.setEchoMode(QLineEdit.Normal)
        else:
            line.setEchoMode(QLineEdit.Password)

    line.setEchoMode(QLineEdit.Password)
    btn.clicked.connect(showPasswordCommand)

    layout.addWidget(label)
    innerLay.addWidget(line)
    innerLay.addWidget(btn)
    layout.addLayout(innerLay)

    return label, line


def AddIntegerEditor(layout, name, maximum=100, minimum=0):
    label = QLabel(name)
    spin = QSpinBox()

    spin.setMaximum(maximum)
    spin.setMinimum(minimum)

    layout.addWidget(label)
    layout.addWidget(spin)

    return label, spin


class ColorButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.color = None
        self.setFlat(True)
        self.setAutoFillBackground(True)
        self.setColor()
        self.clicked.connect(self.pickColor)

    def pickColor(self):
        newColor = QColorDialog.getColor()
        if not newColor.isValid():
            return
        self.setColor(newColor)

    def setColor(self, color=QColor(255, 255, 255)):
        if type(color) == str:
            newColor = QColor()
            newColor.setNamedColor(color)
            color = newColor
        if not color.isValid():
            return
        self.color = color
        pal = self.palette()
        pal.setColor(QPalette.Button, self.color)
        self.setPalette(pal)
        self.update()

    def getColor(self):
        return self.color.name()

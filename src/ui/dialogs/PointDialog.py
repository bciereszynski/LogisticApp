from PyQt5.QtWidgets import QVBoxLayout

from src.common.Point import Point
from src.ui.Editors import AddDecimalEditor, AddIntegerEditor, AddStringEditor
from src.ui.dialogs.ItemDialog import ItemDialog


class PointDialog(ItemDialog):
    def __init__(self):
        self.id = None
        self.lay = QVBoxLayout()

        nameLabel, self.nameLine = AddStringEditor(self.lay, "Name")
        longitudeLabel, self.longitudeSpin = AddDecimalEditor(self.lay, "Longitude")
        latitudeLabel, self.latitudeSpin = AddDecimalEditor(self.lay, "Latitude")
        valueLabel, self.valueSpin = AddIntegerEditor(self.lay, "Value")
        super().__init__(self.lay)
        self.setLayout(self.lay)

    def getItem(self):
        if self.id is None:
            return Point(self.longitudeSpin.value(), self.latitudeSpin.value(), self.valueSpin.value(),
                         self.nameLine.text())
        else:
            return Point(self.longitudeSpin.value(), self.latitudeSpin.value(), self.valueSpin.value(),
                         self.nameLine.text(), self.id)

    def setValues(self, values):
        self.nameLine.setText(values[3])
        self.longitudeSpin.setValue(values[0])
        self.latitudeSpin.setValue(values[1])
        self.valueSpin.setValue(values[2])
        self.id = values[4]

    def resetValues(self):
        self.nameLine.setText("")
        self.longitudeSpin.setValue(0)
        self.latitudeSpin.setValue(0)
        self.valueSpin.setValue(0)
        self.id = None

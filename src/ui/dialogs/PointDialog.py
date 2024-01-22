from PyQt5.QtWidgets import QVBoxLayout

from src.common.Point import Point
from src.ui.Editors import AddDecimalEditor, AddIntegerEditor, AddStringEditor, AddBooleanEditor
from src.ui.dialogs.ItemDialog import ItemDialog


class PointDialog(ItemDialog):
    def __init__(self):
        self.id = None
        self.lay = QVBoxLayout()

        nameLabel, self.nameLine = AddStringEditor(self.lay, "Name")
        longitudeLabel, self.longitudeSpin = AddDecimalEditor(self.lay, "Longitude")
        latitudeLabel, self.latitudeSpin = AddDecimalEditor(self.lay, "Latitude")
        valueLabel, self.valueSpin = AddIntegerEditor(self.lay, "Value")
        isCentralLabel, self.isCentralCheck = AddBooleanEditor(self.lay, "Is central")
        super().__init__(self.lay)
        self.setLayout(self.lay)

    def getItem(self):
        if self.id is None:
            return Point(self.longitudeSpin.value(), self.latitudeSpin.value(), self.valueSpin.value(),
                         self.nameLine.text(), self.isCentralCheck.isChecked())
        else:
            return Point(self.longitudeSpin.value(), self.latitudeSpin.value(), self.valueSpin.value(),
                         self.nameLine.text(), self.isCentralCheck.isChecked(), self.id)

    def setValues(self, values):
        self.nameLine.setText(values[3])
        self.longitudeSpin.setValue(values[0])
        self.latitudeSpin.setValue(values[1])
        self.valueSpin.setValue(values[2])
        self.isCentralCheck.setChecked(values[4])
        self.id = values[5]

    def resetValues(self):
        self.nameLine.setText("")
        self.longitudeSpin.setValue(53.1323)
        self.latitudeSpin.setValue(23.1606)
        self.valueSpin.setValue(0)
        self.isCentralCheck.setChecked(False)
        self.id = None

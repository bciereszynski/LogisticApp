from PyQt5.QtWidgets import QVBoxLayout

from src.common.Courier import Courier
from src.common.Point import Point
from src.ui.Editors import AddDecimalEditor, AddIntegerEditor, AddStringEditor
from src.ui.ItemDialog import ItemDialog


class CourierDialog(ItemDialog):
    def __init__(self):
        self.id = None
        self.lay = QVBoxLayout()

        nameLabel, self.nameLine = AddStringEditor(self.lay, "Name")
        surnameLabel, self.surnameLine = AddStringEditor(self.lay, "Surname")
        emailLabel, self.emailLine = AddStringEditor(self.lay, "Email")
        colorLabel, self.colorLine = AddStringEditor(self.lay, "Color")
        super().__init__(self.lay)
        self.setLayout(self.lay)

    def getItem(self):
        if self.id is None:
            return Courier(self.nameLine.text(), self.surnameLine.text(), self.emailLine.text(),
                           self.colorLine.text())
        else:
            return Courier(self.nameLine.text(), self.surnameLine.text(), self.emailLine.text(),
                           self.colorLine.text(), self.id)

    def setValues(self, values):
        self.nameLine.setText(values[0])
        self.surnameLine.setText(values[1])
        self.emailLine.setText(values[2])
        self.colorLine.setText(values[3])
        self.id = values[4]

    def resetValues(self):
        self.nameLine.setText("")
        self.surnameLine.setText("")
        self.emailLine.setText("")
        self.colorLine.setText("")
        self.id = None

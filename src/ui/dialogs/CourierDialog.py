from PyQt5.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout

from src.common.Courier import Courier
from src.ui.Editors import AddStringEditor, ColorButton
from src.ui.dialogs.ItemDialog import ItemDialog


class CourierDialog(ItemDialog):
    def __init__(self):
        self.id = None
        self.lay = QVBoxLayout()

        nameLabel, self.nameLine = AddStringEditor(self.lay, "Name")
        surnameLabel, self.surnameLine = AddStringEditor(self.lay, "Surname")
        emailLabel, self.emailLine = AddStringEditor(self.lay, "Email")

        self.colorLay = QHBoxLayout()
        colorLabel = QLabel("Color")
        self.colorLay.addWidget(colorLabel)
        self.colorButton = ColorButton()
        self.colorButton.setMaximumSize(25, 25)
        self.colorLay.addWidget(self.colorButton, stretch=0)

        self.lay.addLayout(self.colorLay, stretch=0)

        super().__init__(self.lay)
        self.setLayout(self.lay)

    def getItem(self):
        if self.id is None:
            return Courier(self.nameLine.text(), self.surnameLine.text(), self.emailLine.text(),
                           self.colorButton.getColor())
        else:
            return Courier(self.nameLine.text(), self.surnameLine.text(), self.emailLine.text(),
                           self.colorButton.getColor(), self.id)

    def setValues(self, values):
        self.nameLine.setText(values[0])
        self.surnameLine.setText(values[1])
        self.emailLine.setText(values[2])
        self.colorButton.setColor(values[3])
        self.id = values[4]

    def resetValues(self):
        self.nameLine.setText("")
        self.surnameLine.setText("")
        self.emailLine.setText("")
        self.colorButton.setColor()
        self.id = None

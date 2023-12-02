from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox

from src.calc.AlgorithmConfig import AlgorithmConfig
from src.ui.Editors import AddBooleanEditor


class AlgorithmConfigWindow(QDialog):

    def __init__(self, config: AlgorithmConfig):
        super().__init__()
        self.setWindowTitle("Configure Algorithm")

        self.config = config

        lay = QVBoxLayout()
        self.setLayout(lay)


        TSPLabel, self.TSPCheck = AddBooleanEditor(lay, "TSP")
        InsertLabel, self.InsertCheck = AddBooleanEditor(lay, "Insert")
        ReplaceLabel, self.ReplaceCheck = AddBooleanEditor(lay, "Replace")
        SwapLabel, self.SwapCheck = AddBooleanEditor(lay, "Swap")
        MoveLabel, self.MoveCheck = AddBooleanEditor(lay, "Move")
        RandomConstructLabel, self.RandomConstructCheck = AddBooleanEditor(lay, "Random Construct")
        DisruptLabel, self.DisruptCheck = AddBooleanEditor(lay, "Disrupt")

        self.loadValues()

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save, Qt.Horizontal)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons, Qt.AlignBottom)

    def loadValues(self):
        self.TSPCheck.setChecked(self.config.TSP)
        self.InsertCheck.setChecked(self.config.Insert)
        self.ReplaceCheck.setChecked(self.config.Replace)
        self.SwapCheck.setChecked(self.config.Swap)
        self.MoveCheck.setChecked(self.config.Move)
        self.RandomConstructCheck.setChecked(self.config.RandomConstruct)
        self.DisruptCheck.setChecked(self.config.Disrupt)

    def save(self):
        self.config.TSP = self.TSPCheck.isChecked()
        self.config.Insert = self.InsertCheck.isChecked()
        self.config.Replace = self.ReplaceCheck.isChecked()
        self.config.Swap = self.SwapCheck.isChecked()
        self.config.Move = self.MoveCheck.isChecked()
        self.config.RandomConstruct = self.RandomConstructCheck.isChecked()
        self.config.Disrupt = self.DisruptCheck.isChecked()

        self.close()

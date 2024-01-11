from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox

from src.calc.AlgorithmConfig import AlgorithmConfig
from src.ui.Editors import AddBooleanEditor, AddIntegerEditor


class AlgorithmConfigWindow(QDialog):

    def __init__(self, config: AlgorithmConfig):
        super().__init__()
        self.setWindowTitle("Configure Algorithm")

        self.config = config

        lay = QVBoxLayout()
        self.setLayout(lay)

        LocalLabel, self.LocalEditor = AddIntegerEditor(lay, "Max local iterations")
        TSPLabel, self.TSPCheck = AddBooleanEditor(lay, "2-opt")
        InsertLabel, self.InsertCheck = AddBooleanEditor(lay, "Insert")
        ReplaceLabel, self.ReplaceCheck = AddBooleanEditor(lay, "Replace")
        DisruptLabel, self.DisruptCheck = AddBooleanEditor(lay, "Disrupt")
        AlgLabel, self.AlgEditor = AddIntegerEditor(lay, "Max algorythm iterations")
        PercentLabel, self.PercentEditor = AddIntegerEditor(lay, "Disrupt removal %")

        self.loadValues()

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save, Qt.Horizontal)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons, Qt.AlignBottom)

    def loadValues(self):
        self.LocalEditor.setValue(self.config.MaxLocalLoops)
        self.TSPCheck.setChecked(self.config.TSP)
        self.InsertCheck.setChecked(self.config.Insert)
        self.ReplaceCheck.setChecked(self.config.Replace)
        self.DisruptCheck.setChecked(self.config.Disrupt)
        self.AlgEditor.setValue(self.config.MaxAlgLoops)
        print("test:" ,self.config.DisruptPercent,  self.config.DisruptPercent * 100)
        self.PercentEditor.setValue(round(self.config.DisruptPercent * 100))

    def save(self):
        self.config.MaxLocalLoops = self.LocalEditor.value()
        self.config.TSP = self.TSPCheck.isChecked()
        self.config.Insert = self.InsertCheck.isChecked()
        self.config.Replace = self.ReplaceCheck.isChecked()
        self.config.Disrupt = self.DisruptCheck.isChecked()
        self.config.MaxAlgLoops = self.AlgEditor.value()
        self.config.DisruptPercent = self.PercentEditor.value()/100

        self.close()

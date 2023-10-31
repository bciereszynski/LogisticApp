from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox


class ItemDialog(QDialog):
    def __init__(self, layout):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save, Qt.Horizontal)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getItem(self):
        pass

    def setValues(self, values):
        pass

    def resetValues(self):
        pass

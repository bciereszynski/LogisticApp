from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPlainTextEdit


class RouteDetailsDialog(QDialog):
    def __init__(self, route):
        super().__init__()
        self.setWindowTitle("Route details")

        lay = QVBoxLayout()
        self.setLayout(lay)
        details = "Value: " + str(route.get_value()) + "\n"
        details += "Length: " + str(route.get_length()) + " m \n"
        details += "Route: \n"
        for i, p in enumerate(route.get_points()):
            name = p.name
            name = name.replace("\n", "")
            details += str(i+1) + ". " + name + " " + str(p.value) + "\n"

        self.outputText = QPlainTextEdit()
        lay.addWidget(self.outputText)
        self.outputText.setReadOnly(True)
        self.outputText.setPlainText(details)

        buttons = QDialogButtonBox(QDialogButtonBox.Close, Qt.Horizontal)
        buttons.rejected.connect(self.close)
        lay.addWidget(buttons, Qt.AlignBottom)

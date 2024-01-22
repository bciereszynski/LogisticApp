from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPlainTextEdit


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        lay = QVBoxLayout()
        self.setLayout(lay)

        self.outputText = QPlainTextEdit()
        lay.addWidget(self.outputText)
        self.outputText.setReadOnly(True)
        with open('README.txt', mode="r", encoding="utf-8") as f:
            about = f.read()
        self.outputText.setPlainText(about)

        buttons = QDialogButtonBox(QDialogButtonBox.Close, Qt.Horizontal)
        buttons.rejected.connect(self.close)
        lay.addWidget(buttons, Qt.AlignBottom)

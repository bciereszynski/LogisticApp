from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QMainWindow, QLabel

from src.ui.Editors import AddStringEditor, AddPasswordEditor, AddIntegerEditor


class ConfigWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configure")

        lay = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(lay)
        self.setCentralWidget(widget)

        apiKeyLabel, self.apiKeyEditor = AddStringEditor(lay, "Api key")

        lay.addSpacing(20)
        databaseLabel = QLabel("Database settings")
        lay.addWidget(databaseLabel)

        databaseDriverLabel, self.databaseDriverEditor = AddStringEditor(lay, "Driver")
        databaseNameLabel, self.databaseNameEditor = AddStringEditor(lay, "Name")
        databaseAddressLabel, self.databaseAddressEditor = AddStringEditor(lay, "Address")
        databaseAddressLabel, self.databaseAddressEditor = AddIntegerEditor(lay, "Port")
        databaseLoginLabel, self.databaseLoginEditor = AddStringEditor(lay, "Login")
        databasePasswordLabel, self.databasePasswordEditor = AddPasswordEditor(lay, "Password")

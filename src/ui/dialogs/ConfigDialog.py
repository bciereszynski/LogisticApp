import pickle

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog, QComboBox, QHBoxLayout, QDialogButtonBox

from src.AppConfig import AppConfig
from src.ui.Editors import AddStringEditor, AddPasswordEditor, AddIntegerEditor


class ConfigWindow(QDialog):

    def __init__(self, config: AppConfig):
        super().__init__()
        self.setWindowTitle("Configure")
        self.setFixedSize(600, 300)

        self.config = config

        lay = QHBoxLayout()

        optionalLay = QVBoxLayout()

        apiLay = QVBoxLayout()
        self.apiCombo = QComboBox()
        self.apiCombo.addItem("RapidAPI")
        apiLay.addWidget(self.apiCombo)
        apiKeyLabel, self.apiKeyEditor = AddStringEditor(apiLay, "Api key")
        apiLay.setAlignment(Qt.AlignTop)
        optionalLay.addLayout(apiLay)

        mailLay = QVBoxLayout()
        mailLoginLabel, self.mailLoginEditor = AddStringEditor(mailLay, "Mail login")
        mailPasswordLabel, self.mailPasswordEditor = AddPasswordEditor(mailLay, "Password")
        mailLay.setAlignment(Qt.AlignTop)
        optionalLay.addLayout(mailLay)

        lay.addLayout(optionalLay)
        lay.addSpacing(20)

        databaseLay = QVBoxLayout()
        databaseLabel = QLabel("Database settings")
        databaseLay.addWidget(databaseLabel)

        self.databaseDriverEditor = QComboBox()
        self.databaseDriverEditor.addItem("mariadb+pymysql")
        databaseLay.addWidget(self.databaseDriverEditor)
        databaseNameLabel, self.databaseNameEditor = AddStringEditor(databaseLay, "Name")
        databaseAddressLabel, self.databaseAddressEditor = AddStringEditor(databaseLay, "Address")
        databasePortLabel, self.databasePortEditor = AddIntegerEditor(databaseLay, "Port", 100000)
        databaseLoginLabel, self.databaseLoginEditor = AddStringEditor(databaseLay, "Login")
        databasePasswordLabel, self.databasePasswordEditor = AddPasswordEditor(databaseLay, "Password")

        lay.addLayout(databaseLay)

        self.loadValues()

        verticalLay = QVBoxLayout()
        self.setLayout(verticalLay)

        verticalLay.addLayout(lay)

        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save, Qt.Horizontal)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        verticalLay.addWidget(buttons)

    def loadValues(self):
        try:
            self.apiKeyEditor.setText(self.config.getApiKey())
            self.databaseNameEditor.setText(self.config.databaseName)
            self.databaseAddressEditor.setText(self.config.databaseAddress)
            self.databasePortEditor.setValue(self.config.databasePort)
            self.databaseLoginEditor.setText(self.config.databaseLogin)
            self.databasePasswordEditor.setText(self.config.databasePassword)
            self.mailLoginEditor.setText(self.config.mailLogin)
            self.mailPasswordEditor.setText(self.config.mailPassword)
        except (TypeError, AttributeError):
            pass

    def save(self):
        self.config.setApiKey(self.apiKeyEditor.text())
        self.config.databaseDriver = self.databaseDriverEditor.currentText()
        self.config.databaseName = self.databaseNameEditor.text()
        self.config.databaseAddress = self.databaseAddressEditor.text()
        self.config.databasePort = self.databasePortEditor.value()
        self.config.databaseLogin = self.databaseLoginEditor.text()
        self.config.databasePassword = self.databasePasswordEditor.text()
        self.config.mailLogin = self.mailLoginEditor.text()
        self.config.mailPassword = self.mailPasswordEditor.text()

        self.writeFile()

        self.close()

    def writeFile(self):
        with open("programData/config.cfg", "wb") as outfile:
            pickle.dump(self.config, outfile)

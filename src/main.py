import pickle
import sys

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from AppConfig import AppConfig
from src.data.Repository import Repository
from src.ui.ConfigWindow import ConfigWindow
from PyQt5.QtWidgets import QApplication, QDialog

from src.ui.MainWindow import MainWindow


def initDatabase(config):
    Repository.Engine = create_engine(config.databaseDriver + "://" + config.databaseLogin + ":" +
                                      config.databasePassword + "@" + config.databaseAddress + ":" +
                                      str(config.databasePort) + "/" + config.databaseName)

    Repository.SessionFactory = sessionmaker(bind=Repository.Engine)


def readConfigFile():
    try:
        with open("config.cfg", "rb") as file:
            config = pickle.load(file)
            return config
    except FileNotFoundError:
        return AppConfig()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')

    config = readConfigFile()
    window = None

    while True:
        try:
            initDatabase(config)
            window = MainWindow(config)
            break
        except (SQLAlchemyError, TypeError):
            configWindow = ConfigWindow(config)
            configWindow.exec()

        if configWindow.result() == QDialog.Rejected:
            exit()

    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')



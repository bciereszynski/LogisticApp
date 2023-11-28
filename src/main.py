import pickle
import sys

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.AppConfig import AppConfig
from src.api.DirectionsAPI import DirectionsAPI
from src.api.MatrixAPI import MatrixAPI
from src.data.repositories.Repository import Repository
from src.ui.dialogs.ConfigDialog import ConfigWindow
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


def initCache():
    try:
        with open("directions_cache.dat", "rb") as file:
            requestMap = pickle.load(file)
            DirectionsAPI.requestsMap = requestMap
        with open("matrix_cache.dat", "rb") as file:
            requestMap = pickle.load(file)
            MatrixAPI.requestsMap = requestMap
    except FileNotFoundError:
        pass


def saveCache():
    with open("directions_cache.dat", "wb") as outfile:
        pickle.dump(DirectionsAPI.requestsMap, outfile)
    with open("matrix_cache.dat", "wb") as outfile:
        pickle.dump(MatrixAPI.requestsMap, outfile)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')

    config = readConfigFile()
    initCache()
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
        saveCache()
        print('Closing Window...')



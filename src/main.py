import sys

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.common.AppConfig import AppConfig
from src.data.Repository import Repository
from ui.MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication


def initDatabase(config):
    Repository.Engine = create_engine(config.databaseDriver + "://" + config.databaseLogin + ":" +
                                      config.databasePassword + "@" + config.databaseAddress + ":" +
                                      str(config.databasePort) + "/" + config.databaseName)

    Repository.SessionFactory = sessionmaker(bind=Repository.Engine)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Breeze')

    config = AppConfig()
    config.setApiKey("6daf7a1653msh163f00b78136335p13cdfajsn22dd609d0a86")

    config.databaseLogin = "root"
    config.databasePassword = ""
    config.databaseDriver = "mariadb+pymysql"
    config.databaseAddress = "localhost"
    config.databasePort = 3306
    config.databaseName = "logisticdb"

    initDatabase(config)

    window = MainWindow(config)
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')



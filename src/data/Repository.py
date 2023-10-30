from sqlalchemy import create_engine, String, Column, Integer
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod

class Repository(ABC):
    Engine = create_engine("mariadb+pymysql://root:@localhost:3306/logisticdb")
    SessionFactory = sessionmaker(bind=Engine)

    @abstractmethod
    def GetById(self, identifier):
        pass

    @abstractmethod
    def List(self):
        pass

    @abstractmethod
    def Add(self, item):
        pass

    @abstractmethod
    def Delete(self, item):
        pass

    @abstractmethod
    def Edit(self, item):
        pass

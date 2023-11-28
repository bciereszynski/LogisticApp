from abc import ABC, abstractmethod

class Repository(ABC):
    Engine = None
    SessionFactory = None

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

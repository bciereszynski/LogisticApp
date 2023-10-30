from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def getValues(self):
        pass

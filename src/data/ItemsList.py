import copy

from PyQt5.QtCore import pyqtSignal, QObject


class ItemsList(QObject):
    listChanged = pyqtSignal()

    def __init__(self, repository, itemType):
        super().__init__()
        self.items = []
        self.itemType = itemType
        self.repository = repository

    def fetch(self):
        self.items = self.repository.List()
        self.listChanged.emit()

    def getItems(self):
        return copy.copy(self.items)

    def getItem(self, index):
        return self.items[index]

    def update(self, index, item):
        if type(item) != self.itemType:
            raise Exception("Bad item type")
        if self.items[index].id != item.id:
            raise Exception("Bad item id")
        self.repository.Edit(item)
        self.items[index] = item
        self.listChanged.emit()

    def append(self, item):
        if type(item) != self.itemType:
            raise Exception("Bad item type")
        self.repository.Add(item)
        self.items.append(item)
        self.listChanged.emit()

    def remove(self, item):
        if type(item) != self.itemType:
            raise Exception("Bad item type")
        self.repository.Delete(item)
        self.items.remove(item)
        self.listChanged.emit()

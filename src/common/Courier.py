import uuid

from src.common.Item import Item


class Courier(Item):
    def __init__(self, name: str, surname: str, email: str, color: str, id: uuid = uuid.uuid4()):
        self.id = id
        self.name = name
        self.surname = surname
        self.email = email
        self.color = color

    def getValues(self):
        return [self.name, self.surname, self.email, self.color, self.id]
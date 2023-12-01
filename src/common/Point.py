import math
import uuid

from src.common.Item import Item


class Point(Item):
    __kilometersPerDegree = 73  # For Poland ... 111 for equator

    def __init__(self, longitude: float, latitude: float, value: int, name: str, isCentral: bool = False,
                 Id: uuid = None):
        if Id is None:
            Id = uuid.uuid4()
        self.id = Id
        self.longitude = longitude
        self.latitude = latitude
        self.value = value
        self.name = name
        self.isCentral = isCentral

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def calc_line_distance(self, longitude, latitude):
        point1 = self
        return round(math.sqrt((point1.longitude - longitude) * (point1.longitude - longitude) +
                               (point1.latitude - latitude) * (point1.latitude - latitude))
                     * self.__kilometersPerDegree, 3)

    def get_coordinates_str(self):
        return "%s,%s" % (self.longitude, self.latitude)

    def __str__(self):
        return self.name

    def getValues(self):
        return [self.longitude, self.latitude, self.value, self.name, self.isCentral, self.id]

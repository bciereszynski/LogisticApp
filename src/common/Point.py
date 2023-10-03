import math

class Point:
    __kilometersPerDegree = 73  # For Poland ... 111 for equator

    def __init__(self, longitude: float, latitude: float, value: int, name: str):
        self.longitude = longitude
        self.latitude = latitude
        self.value = value
        self.name = name

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def calc_line_distance(self, point2):
        point1 = self
        return round(math.sqrt((point1.longitude - point2.longitude) * (point1.longitude - point2.longitude) +
                               (point1.latitude - point2.latitude) * (point1.latitude - point2.latitude))
                     * self.__kilometersPerDegree, 3)

    def __str__(self):
        return "%s,%s" % (self.longitude, self.latitude)

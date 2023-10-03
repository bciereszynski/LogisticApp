class Point:
    def __init__(self, long, lat):
        self.longitude = long
        self.latitude = lat

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def __str__(self):
        return "%s,%s" % (self.longitude, self.latitude)

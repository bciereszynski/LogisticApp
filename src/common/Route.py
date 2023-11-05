from src.common.Courier import Courier
from src.common.Point import Point


class Route:
    def __init__(self, central: Point):
        self.points: list[Point] = [central]
        self.courier: Courier = None

    def add(self, point: Point):
        self.points.append(point)

    def get_length(self):
        length = 0
        prevPoint = 0
        for p in self.points:
            if prevPoint != 0:
                length=length+p.calc_line_distance(prevPoint)
            prevPoint = p
        return length

    def get_value(self):
        value = 0
        for p in self.points:
            value=value+p.value
        return value

    def get_plot_data(self):
        longitude = []
        latitude = []
        for p in self.points:
            longitude.append(p.longitude)
            latitude.append(p.latitude)
        return longitude, latitude

    # Function reverses fragment of the list in range [i+1,j] so t[i+1]=t[j] etc.
    # example
    # [1,2,3,4,5,6] 2 4 => [1,2,3,5,4,6]
    def __2opt(self, i, j):
        self.points[i + 1:j + 1] = self.points[i + 1:j + 1][::-1]

    def optimize(self):
        currLength = self.get_length()
        n = len(self.points)
        isImproved = True
        while (isImproved):
            isImproved = False
            for i in range(0, n - 1):  # i=0 ... i<=n-2
                for j in range(i + 1, n):  # j=i+1 ... j<=n-1
                    lengthChange = -self.points[i].calc_line_distance(self.points[(i + 1) % n]) - self.points[j].calc_line_distance(
                        self.points[(j + 1) % n]) + self.points[i].calc_line_distance(self.points[j]) + self.points[(i + 1) % n].calc_line_distance(
                        self.points[(j + 1) % n])

                    if lengthChange < -0.000000000001:  # bcs float!!
                        self.__2opt(i, j)
                        currLength = currLength + lengthChange
                        isImproved = True

from src.common.Courier import Courier
from src.common.Point import Point


class Route:
    def __init__(self, central: Point, distances):
        self.points: list[Point] = [central]
        self.courier: Courier = None
        self.length = 0
        self.distances = distances

    def add(self, point: Point):
        self.length += self.__calculateInsertChange(point, 0)
        self.points.append(point)

    def get_length(self):
        return self.length

    def get_value(self):
        value = 0
        for p in self.points:
            value = value + p.value
        return value

    # Function reverses fragment of the list in range [i+1,j] so t[i+1]=t[j] etc.
    # example
    # [1,2,3,4,5,6] 2 4 => [1,2,3,5,4,6]
    def __2opt(self, i, j):
        self.points[i + 1:j + 1] = self.points[i + 1:j + 1][::-1]

    def __get_distance(self, point1, point2):
        if point1 == point2:
            return 0
        return self.distances[(point1.get_coordinates_str(), point2.get_coordinates_str())]

    def optimize(self):
        n = len(self.points)
        if n < 3:
            return
        isImproved = True
        while (isImproved):
            isImproved = False
            for i in range(0, n - 1):  # i=0 ... i<=n-2
                for j in range(i + 1, n):  # j=i+1 ... j<=n-1
                    lengthChange = (-self.__get_distance(self.points[i], self.points[(i + 1) % n]) -
                                    self.__get_distance(self.points[j], self.points[(j + 1) % n]) +
                                    self.__get_distance(self.points[i], self.points[j]) +
                                    self.__get_distance(self.points[(i + 1) % n], self.points[(j + 1) % n]))

                    # two direction change
                    if lengthChange < -0.000000000001:
                        for x in range(i + 1, j + 1):
                            lengthChange -= self.__get_distance(self.points[x], self.points[(x + 1) % len(self.points)])
                            lengthChange += self.__get_distance(self.points[(x + 1) % len(self.points)], self.points[x])
                    ###

                    if lengthChange < -0.000000000001:  # bcs float!!
                        self.__2opt(i, j)
                        self.length += lengthChange
                        isImproved = True

    def get_plot_data(self):
        longitude = []
        latitude = []
        for p in self.points:
            longitude.append(p.longitude)
            latitude.append(p.latitude)
        return longitude, latitude

    def __calculateInsertChange(self, point, index):
        n = len(self.points)
        if index == 0:
            index = n
        change = (-self.__get_distance(self.points[index - 1], self.points[index % n]) +
                           self.__get_distance(self.points[index - 1], point) +
                           self.__get_distance(point, self.points[index % n]))
        return change

    def check_insert_change(self, point):
        n = len(self.points)
        change = float('inf')
        index = None
        for i in range(1, n + 1):
            localChange = self.__calculateInsertChange(point, i)
            if localChange < change:
                change = localChange
                index = i
        return change, index

    def insert(self, point, index):
        self.points.insert(index, point)
        self.length += self.__calculateInsertChange(point, index)

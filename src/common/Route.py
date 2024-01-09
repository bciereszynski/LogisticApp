from copy import copy

from src.common.Courier import Courier
from src.common.Point import Point


class Route:
    def __init__(self, central: Point, distances):
        self.points: list[Point] = [central]
        self.central = central
        self.courier: Courier = None
        self.length = 0
        self.distances = distances

    def add(self, point: Point):
        self.length += self.__calculate_insert_change(point, 0)
        self.points.append(point)

    def get_points(self):
        points = copy(self.points)
        points.remove(self.central)
        return points
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

                    for x in range(i + 1, j):
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

    def __calculate_insert_change(self, point, index):
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
            localChange = self.__calculate_insert_change(point, i)
            if localChange < change:
                change = localChange
                index = i
        return change, index

    def __check_remove_change(self, point):
        if not self.points.count(point):
            raise Exception("Route doesnt contain that point")
        n = len(self.points)
        index = self.points.index(point)
        if index == 0:
            index = n
        change = (self.__get_distance(self.points[index - 1], self.points[(index + 1) % n]) -
                  self.__get_distance(self.points[index - 1], point) -
                  self.__get_distance(point, self.points[(index + 1) % n]))
        return change

    def insert(self, point, index):
        self.length += self.__calculate_insert_change(point, index)
        self.points.insert(index, point)

    def remove(self, index):
        self.length += self.__check_remove_change(self.points[index])
        self.points.pop(index)

    def calculateCenterOfGravity(self):
        sum_long = 0
        sum_lat = 0
        sum_value = 0
        for p in self.points:
            sum_long += p.longitude * p.value
            sum_lat += p.latitude * p.value
            sum_value += p.value

        return sum_long/sum_value, sum_lat/sum_value

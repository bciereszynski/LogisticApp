import matplotlib.pyplot as plt
from src.data.FileReader import FileReader
import random

from src.common.Point import Point
from src.common.Route import Route

def generateRoutes(points: list[Point], pop_size, t_max):
    routes = []
    central: Point = points[0]
    for i in range(pop_size):
        points_to_delegate = points.copy()
        routes.append(Route(central))
        points_to_delegate.remove(central)
        last = central
        cost = 0
        while len(points_to_delegate)>0:
            rand_point = points_to_delegate[random.randint(0, len(points_to_delegate) - 1)]
            if cost + rand_point.calc_line_distance(last) + rand_point.calc_line_distance(central) < t_max:
                routes[i].add(rand_point)
                cost = cost + rand_point.calc_line_distance(last)
                last = rand_point
            points_to_delegate.remove(rand_point)

    return routes


points: list[Point] = FileReader.read_points('src/data/data.txt')
routes = generateRoutes(points,15,15.23)

for r in routes:
    longitude, latitude = r.get_plot_data()
    plt.plot(longitude, latitude, '-o')
plt.show()

input("opt")

for r in routes:
    r.optimize()
    longitude, latitude = r.get_plot_data()
    plt.plot(longitude, latitude, '-o')
plt.show()

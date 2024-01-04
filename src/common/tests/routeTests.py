from src.common.Point import Point
from src.common.Route import Route


def optimizeBasicTest():
    # given
    central = Point(10, 10, 0, "a")
    point1 = Point(20, 20, 0, "a")
    point2 = Point(10, 20, 0, "a")
    point3 = Point(20, 10, 0, "a")
    distances = {}
    distances[(point1.get_coordinates_str(), point2.get_coordinates_str())] = 10
    distances[(point1.get_coordinates_str(), point3.get_coordinates_str())] = 10
    distances[(point1.get_coordinates_str(), central.get_coordinates_str())] = 15
    distances[(point2.get_coordinates_str(), point1.get_coordinates_str())] = 10
    distances[(point2.get_coordinates_str(), point3.get_coordinates_str())] = 15
    distances[(point2.get_coordinates_str(), central.get_coordinates_str())] = 10
    distances[(point3.get_coordinates_str(), point2.get_coordinates_str())] = 15
    distances[(point3.get_coordinates_str(), point1.get_coordinates_str())] = 10
    distances[(point3.get_coordinates_str(), central.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point2.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point3.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point1.get_coordinates_str())] = 15

    # when
    route = Route(central, distances)
    route.add(point1)
    route.add(point2)
    route.add(point3)

    # assert
    assert route.get_length() == 50
    route.optimize()
    assert route.get_length() == 40


def __calc_length(self):
    length = 0
    for i in range(len(self.points)):
        pair = (self.points[i].get_coordinates_str(), self.points[(i+1)%len(self.points)].get_coordinates_str())
        length += self.distances[pair]
    return length


def optimizeDifferentValuesTest():
    # given
    central = Point(10, 10, 0, "a")
    point1 = Point(20, 20, 0, "a")
    point2 = Point(10, 20, 0, "a")
    point3 = Point(20, 10, 0, "a")
    distances = {}
    distances[(point1.get_coordinates_str(), point2.get_coordinates_str())] = 12
    distances[(point1.get_coordinates_str(), point3.get_coordinates_str())] = 10
    distances[(point1.get_coordinates_str(), central.get_coordinates_str())] = 15
    distances[(point2.get_coordinates_str(), point1.get_coordinates_str())] = 8
    distances[(point2.get_coordinates_str(), point3.get_coordinates_str())] = 15
    distances[(point2.get_coordinates_str(), central.get_coordinates_str())] = 10
    distances[(point3.get_coordinates_str(), point2.get_coordinates_str())] = 15
    distances[(point3.get_coordinates_str(), point1.get_coordinates_str())] = 10
    distances[(point3.get_coordinates_str(), central.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point2.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point3.get_coordinates_str())] = 10
    distances[(central.get_coordinates_str(), point1.get_coordinates_str())] = 15

    # when
    route = Route(central, distances)
    route.add(point1)
    route.add(point2)
    route.add(point3)

    # assert
    assert route.get_length() == 52
    route.optimize()
    assert route.get_length() == __calc_length(route) == 38, str(route.get_length()) + " " + str(__calc_length(route))


optimizeBasicTest()
optimizeDifferentValuesTest()

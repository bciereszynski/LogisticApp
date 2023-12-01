from src.api.MatrixAPI import MatrixAPI
from src.common.Point import Point
from src.common.Route import Route


@staticmethod
def construct(t_max, couriers, points, distances):
    def createStaringRoutes(points_to_delegate):
        routes = []
        dest_point_distance = []
        for dest_point in points_to_delegate:
            dest_point_distance.append(
                (dest_point, distances[(central.get_coordinates_str(), dest_point.get_coordinates_str())]))
        dest_point_distance.sort(reverse=True, key=lambda item: item[1])

        # create routes containing of one furthest point
        for i in range(len(couriers)):
            route = Route(central, distances)
            routes.append(route)

            dest_point = dest_point_distance[i][0]
            route.add(dest_point)
            points_to_delegate.remove(dest_point)
        return routes

    def removeUnreachablePoints(points_to_delegate):
        # filter out all location that cannot be reached
        points_to_delegate.remove(central)
        for p in points_to_delegate.copy():
            if (distances[(p.get_coordinates_str(), central.get_coordinates_str())] +
                    distances[(central.get_coordinates_str(), p.get_coordinates_str())] > t_max):
                points_to_delegate.remove(p)
        if len(points_to_delegate) < len(couriers):
            raise Exception("Unreal conditions")

    central: Point = __findCentral(points)
    points_to_delegate = points.copy()

    removeUnreachablePoints(points_to_delegate)
    routes = createStaringRoutes(points_to_delegate)

    # insert points to routes using the cheapest cost method
    for point in points_to_delegate.copy():
        min_change = float('inf')
        index = None
        selected_route = None
        for route in routes:
            change, i = route.check_insert_change(point)
            if min_change > change and change + route.get_length() <= t_max:
                min_change = change
                index = i
                selected_route = route
        if index is not None:
            selected_route.insert(point, index)
            points_to_delegate.remove(point)

    while len(points_to_delegate) > 0:
        route = Route(central, distances)
        for point in points_to_delegate.copy():
            change, index = route.check_insert_change(point)
            if change + route.get_length() <= t_max:
                route.insert(point, index)
                points_to_delegate.remove(point)
        routes.append(route)

    routes.sort(reverse=True, key=lambda x: x.get_value())
    routes = routes[:len(couriers)]
    for i in range(len(couriers)):
        routes[i].courier = couriers[i]
    return routes, points_to_delegate

    # #
    # random method
    #     while len(points_to_delegate) > 0:
    #         rand_point = points_to_delegate[random.randint(0, len(points_to_delegate) - 1)]
    #         if cost + distances[(rand_point, last)] + distances[(rand_point, central)] < t_max:
    #             route.add(rand_point)
    #             cost = cost + rand_point.calc_line_distance(last)
    #             last = rand_point
    #         points_to_delegate.remove(rand_point)


def __findCentral(points):
    central = None
    for p in points:
        if p.isCentral:
            if central is not None:
                raise Exception("There is more than 1 central")
            else:
                central = p
    if central is None:
        raise Exception("There is no central")
    return central

def TSP(routes):
    for r in routes:
        r.optimize()

def __calc_route_appropriateness(route, points):
    route_appropriateness = []
    cog = route.calculateCenterOfGravity()
    for p in points:
        appropriateness = pow(p.value / p.calc_line_distance(cog[0], cog[1]), 4)
        route_appropriateness.append((p, appropriateness))
    route_appropriateness.sort(key=lambda x: x[1], reverse=True)
    return route_appropriateness

def Insert(routes, points, t_max):
    for r in routes:
        route_appropriateness = __calc_route_appropriateness(r, points)
        for app in route_appropriateness:
            point = app[0]
            change, index = r.check_insert_change(point)
            if r.get_length() + change <= t_max:
                r.insert(point, index)


def runAlgorithm(points, distances_map, t_max, couriers):
    routes, points_to_delegate = construct(t_max, couriers, points, distances_map)

    TSP(routes)
    Insert(routes, points_to_delegate, t_max)

    return routes

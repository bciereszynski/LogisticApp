import requests

from src.AppConfig import AppConfig
from src.api.IApi import IApi

'''
Proxy class to operate api calls, in case of api change make code changes only here
'''


class MatrixAPI(IApi):
    requestsMap = {}

    def __init__(self, config: AppConfig):
        self.url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"
        self.host = "trueway-matrix.p.rapidapi.com"
        self.key = config.getApiKey()

    def get_response(self, points_coordinates):
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        points_string = ""
        for cor in points_coordinates:
            points_string += cor + ';'
        points_string = points_string[:-1]
        querystring = {"origins": points_string,
                       "destinations": points_string}

        response = requests.request(
            "GET", self.url, headers=headers, params=querystring)

        return response

    def get_result(self, points):
        points_coordinates = []
        points.sort(key= lambda x: x.get_name())
        for point in points:
            points_coordinates.append(point.get_coordinates_str())
        points_coordinates = tuple(points_coordinates)
        distancesMap = self.requestsMap.get(points_coordinates)
        if distancesMap is not None:
            return distancesMap
        response = self.get_response(points_coordinates)

        if response.status_code == 429:
            raise Exception("Daily limit exceeded")
        if response.status_code == 403:
            raise Exception("You are not subscribed to this api")
        if response.status_code != 200:
            raise Exception("Unexpected api error: " + str(response.status_code))

        distancesMatrix = response.json()['distances']

        distancesMap = {}
        for i in range(len(points)):
            for j in range(len(points)):
                distancesMap[(points[i].get_coordinates_str(), points[j].get_coordinates_str())] = distancesMatrix[i][j]

        self.requestsMap[points_coordinates] = distancesMap
        return distancesMap

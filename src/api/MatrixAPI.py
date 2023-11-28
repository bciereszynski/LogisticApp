import requests

from src.AppConfig import AppConfig

'''
Proxy class to operate api calls, in case of api change make code changes only here
'''


class MatrixAPI:
    def __init__(self, config: AppConfig):
        self.requestPoints = None
        self.response = None
        self.url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"
        self.host = "trueway-matrix.p.rapidapi.com"
        self.key = config.getApiKey()

    def __get_response(self, points):
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        points_string = ""
        for point in points:
            points_string += str(point) + ';'
        points_string = points_string[:-1]
        querystring = {"origins": points_string,
                       "destinations": points_string}

        response = requests.request(
            "GET", self.url, headers=headers, params=querystring)
        return response

    def get_distances_map(self, points):
        if self.requestPoints != points:
            self.requestPoints = points
            self.response = self.__get_response(points)

        if self.response.status_code == 429:
            raise Exception("Daily limit exceeded")

        distancesMatrix = self.response.json()['distances']

        distancesMap = {}
        for i in range(len(points)):
            for j in range(len(points)):
                distancesMap[(points[i], points[j])] = distancesMatrix[i][j]

        return distancesMap

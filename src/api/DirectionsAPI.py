import requests
import time

from src.AppConfig import AppConfig
from src.api.IApi import IApi

'''
Proxy class to operate api calls, in case of api change make code changes only here
'''


class DirectionsAPI(IApi):
    requestsMap = {}

    def __init__(self, config: AppConfig):
        self.url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        self.host = 'trueway-directions2.p.rapidapi.com'
        self.key = config.getApiKey()

    def get_response(self, points_coordinates):
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        querystring = {
            "stops": f"{points_coordinates[0]};{points_coordinates[1]}"}
        response = requests.request(
            "GET", self.url, headers=headers, params=querystring)
        return response

    def get_result(self, points):
        points_coordinates = (points[0].get_coordinates_str(), points[1].get_coordinates_str())
        coordinates = self.requestsMap.get(points_coordinates)
        if coordinates is not None:
            return coordinates

        response = self.get_response(points_coordinates)
        if response.status_code == 429:
            time.sleep(1.1)
            response = self.get_response(points_coordinates)

        mls = response.json()['route']['geometry']['coordinates']
        coordinates = [(i[0], i[1]) for i in mls]

        self.requestsMap[points_coordinates] = coordinates
        return coordinates

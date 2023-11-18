import requests
import time

from AppConfig import AppConfig

'''
Proxy class to operate api calls, in case of api change make code changes only here
'''


class DirectionsAPI:
    def __init__(self, config: AppConfig):
        self.url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        self.host = 'trueway-directions2.p.rapidapi.com'
        self.key = config.getApiKey()

    def __get_response(self, point1, point2):
        headers = {
            "X-RapidAPI-Key": self.key,
            "X-RapidAPI-Host": self.host
        }
        querystring = {
            "stops": f"{str(point1)};{str(point2)}"}
        response = requests.request(
            "GET", self.url, headers=headers, params=querystring)
        return response

    def get_path_coordinates(self, point1, point2):
        response = self.__get_response(point1, point2)
        if response.status_code == 429:
            time.sleep(1.1)
            response = self.__get_response(point1, point2)
        mls = response.json()['route']['geometry']['coordinates']
        coordinates = [(i[0], i[1]) for i in mls]
        return coordinates

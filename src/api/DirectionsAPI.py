import requests
import time
'''
Proxy class to operate api calls, in case of api change make code changes only here
'''
class DirectionsAPI:
    def __init__(self):
        self.url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        self.key = "6daf7a1653msh163f00b78136335p13cdfajsn22dd609d0a86"
        self.host = 'trueway-directions2.p.rapidapi.com'
    def __get_response(self, point1, point2, mode='drive'):
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
        return None
        response = self.__get_response(point1, point2)
        if response.status_code == 429:
            time.sleep(1.1)
            response = self.__get_response(point1, point2)
        mls = response.json()['route']['geometry']['coordinates']
        coordinates = [(i[0], i[1]) for i in mls]
        return coordinates

import requests

'''
Proxy class to operate api calls, in case of api change make code changes only here
'''
class DirectionsAPI:
    def __get_response(self, point1, point2, mode='drive'):
        url = "https://trueway-directions2.p.rapidapi.com/FindDrivingRoute"
        headers = {
            "X-RapidAPI-Key": "6daf7a1653msh163f00b78136335p13cdfajsn22dd609d0a86",
            "X-RapidAPI-Host": "trueway-directions2.p.rapidapi.com"
        }
        querystring = {
            "stops": f"{str(point1)};{str(point2)}"}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return response

    def get_path_coordinates(self, point1, point2):
        response = self.__get_response(point1, point2)
        mls = response.json()['route']['geometry']['coordinates']
        coordinates = [(i[0], i[1]) for i in mls]
        return coordinates

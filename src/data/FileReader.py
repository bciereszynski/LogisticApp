from src.common.Point import Point


class FileReader:
    @staticmethod
    def read_points(path: str) -> list[Point]:
        with open(path) as f:
            points = []
            for line in f.readlines():
                parts = line.split(" ")
                latitude = float(parts[1])
                longitude = float(parts[0])
                value = int(parts[2])
                name = parts[3]
                points.insert(len(points), Point(longitude, latitude, value, name))

        return points

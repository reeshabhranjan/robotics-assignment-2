from math import sqrt
from typing import List

from matplotlib import pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def norm(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    def __cmp__(self, other):
        point_diff = self - other
        return point_diff.x * point_diff.y

    def to_tuple(self):
        return self.x, self.y


class Circle:
    def __init__(self, center: Point, radius: float):
        assert type(center) == Point
        self.center = center
        self.radius = radius

    def __str__(self):
        return f'center = {self.center}, radius = {self.radius}'


class LineSegment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f'start = {self.start}, end = {self.end}'

    def length(self) -> float:
        return (self.start - self.end).norm()

    def distance_from_point(self, point: Point) -> float:
        a = self.length()
        b = self.start.dist(point)
        c = self.end.dist(point)
        s = (a + b + c) / 2
        area = sqrt(s * (s - a) * (s - b) * (s - c))
        distance = (2 * area) / a
        return distance

    def intersects_circle(self, circle: Circle):
        if self.distance_from_point(circle.center) <= circle.radius:
            if circle.center.dist(self.start) <= circle.radius or circle.center.dist(self.end) <= circle.radius:
                return True
            else:
                del_start_x = circle.center.x - self.start.x
                del_start_y = circle.center.y - self.start.y
                del_end_x = circle.center.x - self.end.x
                del_end_y = circle.center.y - self.end.y

                if del_start_x * del_end_x <= 0 or del_start_y * del_end_y <= 0:
                    return True
                else:
                    return False
        else:
            return False


class Graph:
    def __init__(self, config):
        self.range_start = Point(config["graph"]["xlim"][0], config["graph"]["ylim"][0])
        self.range_end = Point(config["graph"]["xlim"][1], config["graph"]["ylim"][1])
        self.obstacles = [Circle(Point(obstacle["center"][0], obstacle["center"][1]), obstacle["radius"])
                          for obstacle in config["graph"]["obstacles"]]
        self.lines: List[LineSegment] = []
        self.paths: List[LineSegment] = []
        self.start_point: Point = None
        self.end_point: Point = None
        self.points: List[Point] = []
        self.continuous_x: List[float] = None
        self.continuous_y: List[float] = None

    def show_plot(self):
        figure, axes = plt.subplots()
        plt.xlim([self.range_start.x, self.range_end.x])
        plt.ylim([self.range_start.y, self.range_end.y])

        for obstacle in self.obstacles:
            circle = plt.Circle(obstacle.center.to_tuple(), obstacle.radius)
            axes.add_artist(circle)

        for line in self.lines:
            axes.plot((line.start.x, line.end.x), (line.start.y, line.end.y), 'g')

        for path in self.paths:
            axes.plot((path.start.x, path.end.x), (path.start.y, path.end.y), 'r')

        for point in self.points:
            axes.plot(point.x, point.y, 'ro')

        if self.start_point is not None:
            axes.plot(self.start_point.x, self.start_point.y, 'rx')

        if self.end_point is not None:
            axes.plot(self.end_point.x, self.end_point.y, 'rx')

        if self.continuous_x is not None and self.continuous_y is not None:
            axes.plot(self.continuous_x, self.continuous_y, 'r')

        plt.show()

    def add_line(self, line: LineSegment):
        self.lines.append(line)

    def add_point(self, point: Point):
        self.points.append(point)

    def set_continuous_path(self, continuous_x, continuous_y):
        self.continuous_x = continuous_x
        self.continuous_y = continuous_y

    def add_path(self, path: LineSegment):
        self.paths.append(path)

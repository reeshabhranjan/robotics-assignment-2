import os
from math import sqrt
from typing import List

import numpy as np
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
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            return Point(self.x + other, self.y + other)

    def __mul__(self, other):  # TODO add support for piecewise multiplication
        return Point(other * self.x, other * self.y)

    def __radd__(self, other):
        return self + other

    def __truediv__(self, other):
        if other == 0:
            return Point(float("inf"), float("inf"))
        else:
            return Point(self.x / other, self.y / other)

    __rmul__ = __mul__

    def norm(self):
        return sqrt((self.x ** 2) + (self.y ** 2))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash(str(self))

    def to_tuple(self):
        return self.x, self.y

    def slope(self):
        if self.x != 0:
            return self.y / self.x
        return np.sign(self.y) * float("inf")


class Circle:
    def __init__(self, center: Point, radius: float):
        assert isinstance(center, Point)
        self.center = center
        self.radius = radius

    def contains_point(self, point: Point):
        return self.center.dist(point) <= self.radius

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
        self.continuous_path: List[Point] = []
        self.arrows: List[LineSegment] = []

    def plot(self, filename: str):
        figure, axes = plt.subplots()
        plt.xlim([self.range_start.x, self.range_end.x])
        plt.ylim([self.range_start.y, self.range_end.y])

        for obstacle in self.obstacles:
            circle = plt.Circle(obstacle.center.to_tuple(), obstacle.radius)
            axes.add_artist(circle)

        for line in self.lines:
            axes.plot((line.start.x, line.end.x), (line.start.y, line.end.y), color='g', linewidth=2)

        for path in self.paths:
            axes.plot((path.start.x, path.end.x), (path.start.y, path.end.y), 'r--')

        for point in self.points:
            axes.plot(point.x, point.y, 'ro')

        if self.start_point is not None:
            axes.plot(self.start_point.x, self.start_point.y, 'gx')

        if self.end_point is not None:
            axes.plot(self.end_point.x, self.end_point.y, 'rx')

        if len(self.continuous_path) > 0:
            continuous_x = [point.x for point in self.continuous_path]
            continuous_y = [point.y for point in self.continuous_path]
            axes.plot(continuous_x, continuous_y, 'r')

        for arrow in self.arrows:
            axes.arrow(arrow.start.x, arrow.start.y, arrow.end.x, arrow.end.y)
        plot_dir = "plots/"

        axes.title

        if not os.path.isdir(plot_dir):
            os.mkdir(plot_dir)
        filepath = f'{plot_dir}{filename}.png'
        plt.savefig(filepath)

    def add_arrow(self, from_point: Point, to_point: Point):
        arrow = LineSegment(from_point, to_point)
        self.arrows.append(arrow)

    def add_line(self, line: LineSegment):
        self.lines.append(line)

    def add_point(self, point: Point):
        self.points.append(point)

    def add_point_to_continuous_path(self, point: Point):
        self.continuous_path.append(point)

    def add_path(self, path: LineSegment):
        self.paths.append(path)


class Tree:
    def __init__(self, root: Point):
        self.parents = {root: None}
        self.root = root
        self.counter = 0

    def nodes(self):
        return self.parents

    def insert(self, new_point: Point, parent_point: Point):
        assert parent_point in self.nodes()
        self.parents[new_point] = parent_point

    def __sub__(self, other):
        min_dist = float("inf")
        for self_node in self.nodes():
            for other_node in other.nodes():
                min_dist = min(min_dist, self_node.dist(other_node))
        return min_dist

    def get_closest_pair(self, other):
        min_dist = float("inf")
        self_node_min = None
        other_node_min = None
        for self_node in self.nodes():
            for other_node in other.nodes():
                if self_node.dist(other_node) < min_dist:
                    min_dist = self_node.dist(other_node)
                    self_node_min = self_node
                    other_node_min = other_node
        return self_node_min, other_node_min

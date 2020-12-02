import os
from math import sqrt
from typing import List

import numpy as np
from matplotlib import pyplot as plt


class Point:
    """
    This is the 2D point class. It takes in float values for the x and y-coordinates.
    To avoid precision errors, it rounds off values to 3 decimal places.
    Similarly, for equating two points, I have checked the distance between the points
    upto a threshold until which I can tell if they are same or different points.
    """

    def __init__(self, x, y):
        self.x = round(x, 3)
        self.y = round(y, 3)

    def dist(self, other) -> float:
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return str(self)

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
        return abs(self.x - other.x) <= 0.01 and abs(self.y - other.y) <= 0.01

    def __ne__(self, other):
        return abs(self.x - other.x) > 0.01 or abs(self.y - other.y) > 0.01

    def __hash__(self):
        return hash(str(self))

    def to_tuple(self):
        return self.x, self.y

    def slope(self):
        if self.x != 0:
            return self.y / self.x
        return np.sign(self.y) * float("inf")


class Circle:
    """
    This is the 2D-circle class. It takes in a Point object as the center and a
    float object as the radius.
    """

    def __init__(self, center: Point, radius: float):
        assert isinstance(center, Point)
        self.center = center
        self.radius = radius

    def contains_point(self, point: Point):
        """
        This function checks if the circle contains the point.
        :param point:
        :return: bool
        """
        return self.center.dist(point) <= self.radius

    def __str__(self):
        return f'center = {self.center}, radius = {self.radius}'


class LineSegment:
    """
    This is a 2D-line class. It takes in two Point objects as the endpoints of
    the line.
    """

    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __str__(self):
        return f'start = {self.start}, end = {self.end}'

    def length(self) -> float:
        """
        Returns length of the line.
        :return: float
        """
        return (self.start - self.end).norm()

    def slope(self) -> float:
        """
        Returns slope of the line.
        :return: float
        """
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def distance_from_point(self, point: Point) -> float:
        """
        Returns the perpendicular distance from a point.
        :param point:
        :return: float
        """
        a = self.length()
        b = self.start.dist(point)
        c = self.end.dist(point)
        s = (a + b + c) / 2
        area = sqrt(s * (s - a) * (s - b) * (s - c))
        distance = (2 * area) / a
        return distance

    def intersects_circle(self, circle: Circle):
        """
        Checks if the current line segment intersects with a circle.
        :param circle:
        :return: bool
        """
        if self.distance_from_point(circle.center) <= circle.radius:
            if circle.center.dist(self.start) <= circle.radius or circle.center.dist(self.end) <= circle.radius:
                return True
            else:
                slope_line = self.slope()
                sign_start_point = (self.start.y - circle.center.y) * slope_line + (self.start.x - circle.center.x)
                sign_end_point = (self.end.y - circle.center.y) * slope_line + (self.end.x - circle.center.x)
                return sign_end_point * sign_start_point <= 0
        else:
            return False


class Graph:
    """
    This is the Graph class. It is initialized using a configuration dictionary.
    It can contain all types of objects (Point, Circle, Line) in a graph.
    It also has a function plot() that will save the current state of the graph
    as a PNG image to the plots/ subdirectory.
    """

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
        """
        Plots the state of the graph into a file.
        :param filename:
        :return: None
        """
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
            axes.text(self.start_point.x, self.start_point.y, 'start')

        if self.end_point is not None:
            axes.plot(self.end_point.x, self.end_point.y, 'rx')
            axes.text(self.end_point.x, self.end_point.y, 'end')

        if len(self.continuous_path) > 0:
            continuous_x = [point.x for point in self.continuous_path]
            continuous_y = [point.y for point in self.continuous_path]
            axes.plot(continuous_x, continuous_y, 'r')

        for arrow in self.arrows:
            axes.arrow(arrow.start.x, arrow.start.y, arrow.end.x, arrow.end.y)
        plot_dir = "plots/"

        axes.title.set_text(filename)

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
    """
    This is the Tree class. It implements a Tree structure where the nodes
    are of type Point. In order to maintain the structure, a dictionary named
    parents is defined. It defines the mapping from child to its parent node (point).
    In order to allow Point to support hashing, a __hash__ and __eq__ is defined in
    the Point class.
    """

    def __init__(self, root: Point):
        self.parents = {root: None}
        self.root = root
        self.counter = 0

    def nodes(self):
        """
        Returns an iterable of the nodes in this tree.
        :return: dict
        """
        return self.parents

    def insert(self, new_point: Point, parent_point: Point):
        """
        Inserts a new point into the current tree.
        :param new_point:
        :param parent_point:
        :return: None
        """
        assert parent_point in self.nodes()
        self.parents[new_point] = parent_point

    def __sub__(self, other) -> float:
        """
        Returns the shortest distance between two trees regardless of obstacles.
        :param other:
        :return: float
        """
        min_dist = float("inf")
        for self_node in self.nodes():
            for other_node in other.nodes():
                min_dist = min(min_dist, self_node.dist(other_node))
        return min_dist

    def get_closest_pair(self, other):
        """
        Returns the pair of points in two trees closes to each other regardlesso
        of obstacles.
        :param other:
        :return: tuple(Point, Point)
        """
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

    def get_shortest_clear_path_to_point(self, point: Point, obstacles: List[Circle]) -> Point:
        """
        Returns the point in the current tree closes to a given point considering all the
        obstacles. Returns None if no such point exists.
        :param point:
        :param obstacles:
        :return:
        """
        closest_node = None
        closes_distance = float("inf")
        for node in self.nodes():
            line_joining = LineSegment(node, point)
            if any([line_joining.intersects_circle(obstacle) for obstacle in obstacles]):
                continue
            if node.dist(point) < closes_distance:
                closes_distance = node.dist(point)
                closest_node = node
        return closest_node

    def __str__(self):
        return f'Tree with root {self.root}'

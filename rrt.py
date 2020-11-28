from math import atan2, sin, cos
from random import random

from graph import Graph, Point, Tree, LineSegment


class RRT:
    def __init__(self, config):
        self.graph: Graph = Graph(config)
        self.start = Point(config["rrt"]["start"][0], config["rrt"]["start"][1])
        self.end = Point(config["rrt"]["end"][0], config["rrt"]["end"][1])
        self.iters = config["rrt"]["iters"]
        self.delta = config["rrt"]["delta"]
        self.tree_start = Tree(self.start)
        self.tree_end = Tree(self.end)

    def bidirectional_rrt(self):
        self.__rrt(self.tree_start)
        self.graph.show_plot()

    def __rrt(self, tree: Tree):
        i = 0
        while i < self.iters:
            new_point = self.__get_random_point()
            nearest_point = min(tree.nodes(), key=lambda x: new_point.dist(x))
            diff_point = new_point - nearest_point
            theta = atan2(diff_point.y, diff_point.x)
            delta_point = Point(nearest_point.x + self.delta * sin(theta),
                                nearest_point.y + self.delta * cos(theta))
            joining_line = LineSegment(nearest_point, delta_point)
            if self.__line_collides_with_obstacles(joining_line):
                continue
            i += 1
            self.graph.add_line(joining_line)
            self.graph.add_point(tree.root)
            tree.insert(delta_point, nearest_point)

    def __get_random_point(self) -> Point:
        rand_x = self.start.x + random() * (self.end.x - self.start.x)
        rand_y = self.start.y + random() * (self.end.y - self.start.y)
        return Point(rand_x, rand_y)

    def __line_collides_with_obstacles(self, line: LineSegment):
        for obstacle in self.graph.obstacles:
            if line.intersects_circle(obstacle):
                return True
        return False

from math import atan2, sin, cos
from random import random

from graph import Graph, Point, Tree, LineSegment


class RRT:
    def __init__(self, config):
        self.start = Point(config["rrt"]["start"][0], config["rrt"]["start"][1])
        self.end = Point(config["rrt"]["end"][0], config["rrt"]["end"][1])
        self.iters = config["rrt"]["iters"]
        self.delta = config["rrt"]["delta"]
        self.tree_start = Tree(self.start)
        self.tree_end = Tree(self.end)

        self.graph: Graph = Graph(config)
        self.graph.start_point = self.start
        self.graph.end_point = self.end

    def bidirectional_rrt(self):
        for i in range(self.iters):
            # TODO fix algo
            self.__expand_tree(self.tree_start)
            self.__expand_tree(self.tree_end)
            if self.tree_start - self.tree_end < self.delta:  # TODO optimise this to O(n)
                joining_point_start, joining_point_end = self.tree_start.get_closest_pair(self.tree_end)
                joining_line = LineSegment(joining_point_start, joining_point_end)
                self.graph.add_path(joining_line)
                self.__generate_path(self.tree_start, joining_point_start)
                self.__generate_path(self.tree_end, joining_point_end)
                break
        self.graph.plot('rrt')

    def __expand_tree(self, tree: Tree):  # TODO fix when line gets out of bounds
        valid = False
        while not valid:
            new_point = self.__get_random_point()
            nearest_point = min(tree.nodes(), key=lambda x: new_point.dist(x))
            diff_point = new_point - nearest_point
            theta = atan2(diff_point.y, diff_point.x)
            delta_point = Point(nearest_point.x + self.delta * sin(theta),
                                nearest_point.y + self.delta * cos(theta))
            joining_line = LineSegment(nearest_point, delta_point)
            if self.__line_collides_with_obstacles(joining_line):
                continue
            valid = True
            self.graph.add_line(joining_line)
            self.graph.add_point(delta_point)
            tree.insert(delta_point, nearest_point)

    def __generate_path(self, tree, leaf):
        node = leaf
        # while tree.parents[node] is not None:
        while tree.root != node:
            joining_line = LineSegment(node, tree.parents[node])
            self.graph.add_path(joining_line)
            node = tree.parents[node]

    def __get_random_point(self) -> Point:
        rand_x = self.start.x + random() * (self.end.x - self.start.x)
        rand_y = self.start.y + random() * (self.end.y - self.start.y)
        return Point(rand_x, rand_y)

    def __line_collides_with_obstacles(self, line: LineSegment):
        for obstacle in self.graph.obstacles:
            if line.intersects_circle(obstacle):
                return True
        return False

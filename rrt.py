from math import atan2, sin, cos
from random import random

from graph import Graph, Point, Tree, LineSegment


class RRT:
    """
    This class contains all the data related to RRT algo.
    """

    def __init__(self, config):
        self.start = Point(config["rrt"]["start"][0], config["rrt"]["start"][1])
        self.end = Point(config["rrt"]["end"][0], config["rrt"]["end"][1])
        self.delta = config["rrt"]["delta"]
        self.tree_start = Tree(self.start)
        self.tree_end = Tree(self.end)

        self.graph: Graph = Graph(config)
        self.graph.start_point = self.start
        self.graph.end_point = self.end

    def bidirectional_rrt(self):
        """
        Runs the bidirectional RRT and saves the plot to a file.
        :return:
        """
        connected = False
        expand_tree_start = True
        while not connected:
            if expand_tree_start:
                new_point = self.__expand_tree(self.tree_start)
            else:
                new_point = self.__expand_tree(self.tree_end)

            if expand_tree_start:
                joining_point = self.tree_end.get_shortest_clear_path_to_point(new_point, self.graph.obstacles)
            else:
                joining_point = self.tree_start.get_shortest_clear_path_to_point(new_point, self.graph.obstacles)

            if joining_point is not None:
                if expand_tree_start:
                    joining_point_start = new_point
                    joining_point_end = joining_point
                else:
                    joining_point_start = joining_point
                    joining_point_end = new_point
                joining_line = LineSegment(joining_point_start, joining_point_end)
                self.graph.add_path(joining_line)
                self.__generate_path(self.tree_start, joining_point_start)
                self.__generate_path(self.tree_end, joining_point_end)
                connected = True
            expand_tree_start = not expand_tree_start
        self.graph.plot('rrt')

    def __expand_tree(self, tree: Tree):  # TODO fix when line gets out of bounds
        """
        Inserts one new node to a given tree as per RRT.
        :param tree:
        :return:
        """

        while True:
            random_point = self.__get_random_point()
            nearest_point = min(tree.nodes(), key=lambda x: random_point.dist(x))
            if random_point.dist(nearest_point) <= self.delta:
                delta_point = random_point
            else:
                diff_point = random_point - nearest_point
                theta = atan2(diff_point.y, diff_point.x)
                delta_point = Point(nearest_point.x + self.delta * cos(theta),
                                    nearest_point.y + self.delta * sin(theta))
            joining_line = LineSegment(nearest_point, delta_point)
            if self.__line_collides_with_obstacles(joining_line):
                continue
            self.graph.add_line(joining_line)
            self.graph.add_point(delta_point)
            tree.insert(delta_point, nearest_point)
            return delta_point

    def __generate_path(self, tree, leaf):
        """
        Generates the path from the leaf to the tree in the graph.
        :param tree:
        :param leaf:
        :return:
        """
        node = leaf
        # while tree.parents[node] is not None:
        while tree.root != node:
            joining_line = LineSegment(node, tree.parents[node])
            self.graph.add_path(joining_line)
            node = tree.parents[node]

    def __get_random_point(self) -> Point:
        """
        Returns a random point as per the bounds of the current graph limits.
        :return:
        """
        rand_x = self.start.x + random() * (self.end.x - self.start.x)
        rand_y = self.start.y + random() * (self.end.y - self.start.y)
        return Point(rand_x, rand_y)

    def __line_collides_with_obstacles(self, line: LineSegment):
        """
        Checks if a line collides with any obstacle or not.
        :param line:
        :return:
        """

        return any([line.intersects_circle(obstacle) for obstacle in self.graph.obstacles])

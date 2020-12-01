import numpy as np

from graph import Graph, Point, Circle


class APF:
    def __init__(self, config, paraboloid=True):
        self.graph = Graph(config)
        self.rois = config["apf"]["rois"]
        assert len(self.rois) == len(self.graph.obstacles)
        self.start = Point(config["rrt"]["start"][0], config["rrt"]["start"][1])
        self.end = Point(config["rrt"]["end"][0], config["rrt"]["end"][1])
        self.ka = config["apf"]["ka"]
        self.kr = config["apf"]["kr"]
        self.gamma = config["apf"]["gamma"]
        self.convergence_delta = config["apf"]["convergence_delta"]
        self.graph.start_point = self.start
        self.graph.end_point = self.end
        self.paraboloid = paraboloid

    def apf(self):
        point = self.start
        while point.dist(self.end) > self.convergence_delta:
            point = point - self.__get_total_potential_derivative(point)
            self.graph.add_point_to_continuous_path(point)
        if self.paraboloid:
            graph_name = 'apf_paraboloid'
        else:
            graph_name = 'apf_conical'
        self.graph.plot(graph_name)

    def __get_total_potential_derivative(self, point) -> Point:
        repulsive_potential_derivatives = [self.__repulsive_potential_derivative(point, obstacle, roi) for
                                           (obstacle, roi) in
                                           zip(self.graph.obstacles, self.rois)]
        attractive_potential_derivative = self.__attractive_potential_derivative(point)
        net_potential_derivative = sum(repulsive_potential_derivatives) + attractive_potential_derivative
        return net_potential_derivative

    def __attractive_potential_derivative(self, point: Point) -> Point:
        if self.paraboloid:
            derivative = Point(
                -self.ka * (self.end.x - point.x),
                -self.ka * (self.end.y - point.y)
            )
        else:
            derivative = Point(
                -self.ka * np.sign(self.end.x - point.x),
                -self.ka * np.sign(self.end.y - point.y)
            )
        return derivative

    def __repulsive_potential_derivative(self, point: Point, obstacle: Circle, roi) -> Point:
        distance_from_boundary = point.dist(obstacle.center) - obstacle.radius
        if distance_from_boundary > roi:
            return Point(0, 0)
        # TODO removed negative sign
        e = point - obstacle.center
        e = e / e.norm()
        derivative = self.kr * pow((1 / distance_from_boundary - 1 / roi), self.gamma - 1) / pow(
            distance_from_boundary, 2) * e
        return derivative

    def __get_repulsive_potential(self, point: Point, obstacle: Circle) -> Point:
        distance_from_boundary = point.dist(obstacle.center) - obstacle.radius
        if distance_from_boundary > self.rois:
            return Point(0, 0)
        potential = (self.ka / self.gamma) * pow((1 / distance_from_boundary - 1 / self.rois), self.gamma)
        return potential

    def __get_total_potential(self, point: Point) -> float:
        # TODO
        pass

    def __attractive_potential(self, point: Point) -> float:
        # TODO
        pass

import numpy as np

from graph import Graph, Point, Circle


class APF:
    def __init__(self, config, paraboloid=True):
        self.graph = Graph(config)
        self.roi = config["apf"]["roi"]
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
        repulsive_potential_derivatives = [self.__repulsive_potential_derivative(point, obstacle) for obstacle in
                                           self.graph.obstacles]
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

    def __repulsive_potential_derivative(self, point: Point, obstacle: Circle) -> Point:
        distance_from_boundary = point.dist(obstacle.center) - obstacle.radius
        if distance_from_boundary > self.roi:
            return Point(0, 0)
        derivative = -self.kr * pow((1 / distance_from_boundary - 1 / self.roi), self.gamma - 1) / pow(
            distance_from_boundary, 2) * (point - obstacle.center)
        return derivative

    def __get_repulsive_potential(self, point: Point, obstacle: Circle) -> Point:
        distance_from_boundary = point.dist(obstacle.center) - obstacle.radius
        if distance_from_boundary > self.roi:
            return Point(0, 0)
        potential = (self.ka / self.gamma) * pow((1 / distance_from_boundary - 1 / self.roi), self.gamma)
        return potential

    def __get_total_potential(self, point: Point) -> float:
        # TODO
        pass

    def __attractive_potential(self, point: Point) -> float:
        # TODO
        pass

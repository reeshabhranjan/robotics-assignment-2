from math import sqrt


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


class Circle:
    def __init__(self, center: Point, radius: float):
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

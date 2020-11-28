from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Circle:
    def __init__(self, center: Point, radius):
        self.center = center
        self.radius = radius


class LineSegment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __len__(self):
        return self.start.dist(self.end)

    def distance(self, point: Point):
        a = len(self)
        b = self.start.dist(point)
        c = self.end.dist(point)
        s = (a + b + c) / 2
        area = sqrt(s * (s - a) * (s - b) * (s - c))
        distance = (2 * area) / a
        return distance

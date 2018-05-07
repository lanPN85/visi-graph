from collections import namedtuple

import numpy as np
import math

Point = namedtuple('Point', ['x', 'y'])


class HalfLine:
    def __init__(self, origin: Point, angle=0.):
        self._origin = origin
        self._angle = angle % 360.

    @property
    def origin(self) -> Point:
        return self._origin

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def incl_angle(self) -> float:
        agl = self.angle % 180.
        if agl > 90:
            agl = - (180 - agl)
        return agl

    @property
    def coeffs(self):
        """
        Calculates a, b, c for the line equation ax + by + c = 0
        :return: A tuple (a, b, c)
        """
        if self.incl_angle == 90. or self.incl_angle == -90.:
            return 1., 0., -self.origin.x
        else:
            slope = math.tan(math.radians(self.incl_angle))
            k = slope * self.origin.x - self.origin.y
            return -slope, 1., k

    def __contains__(self, item: Point):
        if item == self.origin:
            return True

        hl = HalfLine.from_points(self.origin, item)
        return self.angle == hl.angle

    @classmethod
    def from_points(cls, origin: Point, target: Point):
        if origin == target:
            raise ValueError('Cannot create half line from 2 identical points')
        line = LineSegment(origin, target)

        if origin.y > target.y:
            if origin.x == target.x:
                angle = 90.
            elif origin.x < target.x:
                angle = math.degrees(math.asin((origin.y - target.y) / line.length))
            else:
                angle = 90. + math.degrees(math.acos((origin.y - target.y) / line.length))
        elif origin.y < target.y:
            if origin.x == target.x:
                angle = 270.
            elif origin.x > target.x:
                angle = 180. + math.degrees(math.asin((target.y - origin.y) / line.length))
            else:
                angle = 270. + math.degrees(math.acos((target.y - origin.y) / line.length))
        else:
            if origin.x > target.x:
                angle = 180.
            else:
                angle = 0.
        return cls(origin, angle)


class LineSegment:
    def __init__(self, p1: Point, p2: Point):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self) -> Point:
        return self._p1

    @property
    def p2(self) -> Point:
        return self._p2

    @property
    def coeffs(self):
        """
        Calculates a, b, c for the line equation ax + by + c = 0
        :return: A tuple (a, b, c)
        """
        try:
            _a = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
            _b = self.p1.y - _a * self.p1.x
            a, b, c = _a, -1, _b
            return a, b, c
        except ZeroDivisionError:
            return 1, 0, -self.p1.x

    @property
    def length(self):
        """
        :return: The segment's length, a.k.a the Euclidean distance between its endpoints.
        """
        ln = math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)
        return ln

    def __eq__(self, other):
        if not isinstance(other, LineSegment):
            return False
        return (self.p1 == other.p1 and self.p2 == other.p2) or (self.p1 == other.p2 and self.p2 == other.p1)

    def __repr__(self):
        return 'LineSegment(%s, %s)' % (self.p1, self.p2)

    def __contains__(self, p: Point):
        eps = 1e-4

        # Round out input to avoid alignment mistakes
        p = Point(np.around(p.x, 5), np.around(p.y, 5))

        a, b, c = self.coeffs
        inx = min(self.p1.x, self.p2.x) - eps <= p.x <= max(self.p1.x, self.p2.x) + eps
        iny = min(self.p1.y, self.p2.y) - eps <= p.y <= max(self.p1.y, self.p2.y) + eps
        aligned = abs(a * p.x + b * p.y + c) < eps
        return inx and iny and aligned

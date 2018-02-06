from collections import namedtuple
from typing import List

import math
import sys
import numpy as np

Point = namedtuple('Point', ['x', 'y'])


class LineSegment:
    def __init__(self, p1: Point, p2: Point):
        self._p1 = p1
        self._p2 = p2

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
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


class Polygon:
    def __init__(self, vertices: List[Point]):
        """
        Initialize a new Polygon from a list of Points. Polygons are immutable.
        :param vertices: A list of Point that describes how to construct the Polygon.
        """
        if vertices[0] == vertices[-1]:
            vertices = vertices[:-1]
        self._vertices = tuple(vertices)

        # Construct edge list from vertices
        self._edges = []
        for prev, current in zip(vertices[:-1], vertices[1:]):
            self._edges.append(LineSegment(prev, current))
        self._edges.append(LineSegment(vertices[-1], vertices[0]))

    def __contains__(self, item):
        return item in self.edges or item in self.vertices

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def impact_points(self, line: LineSegment):
        """
        Calculates points where the polygon and a line segment meets.
        :param line: A line segment
        :return: A set of Coordinate of impact points, or None if there are none.
        """
        from vsg import functional
        return functional.impact_points(self, line)


_AdjacentNode = namedtuple('Node', ['coord', 'w'])


class VisibilityGraph:
    def __init__(self, s: Point, t: Point, segments=None):
        self._s, self._t = s, t
        self._segments = list() if segments is None else segments
        self._adj = None
        self._vertices = None

    def construct_adj_list(self):
        """
        Constructs the graph's adjacency list based on its segments.
        Should be done after the graph's segments have been fully added.
        """
        if self.constructed:
            print('WARNING: Overriding existing edge list.', file=sys.stderr)

        self._vertices = set()
        for s in self._segments:
            self._vertices.add(s.p1)
            self._vertices.add(s.p2)
        self._vertices = list(self._vertices)

        self._adj = {}
        for v in self._vertices:
            self._adj[v] = []

        for s in self._segments:
            self._adj[s.p1].append(_AdjacentNode(coord=s.p2, w=s.length))
            self._adj[s.p2].append(_AdjacentNode(coord=s.p1, w=s.length))

    @property
    def segments(self):
        return tuple(self._segments)

    def add_segment(self, segment: LineSegment):
        """
        Adds a segment to the graph. No op if the segment is already in the graph.
        :param segment: A LineSegment
        """
        if segment not in self.segments:
            self._segments.append(segment)

    @property
    def constructed(self):
        return self._adj is not None and self._vertices is not None

    @property
    def adjacent_list(self):
        return self._adj

    @property
    def vertices(self):
        return tuple(self._vertices)

    @property
    def start(self):
        return self._s

    @property
    def end(self):
        return self._t

from collections import namedtuple
from typing import List

import math
import sys

Coordinate = namedtuple('Coordinate', ['x', 'y'])


class LineSegment:
    def __init__(self, p1: Coordinate, p2: Coordinate):
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
        a = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
        b = self.p1.y - a * self.p1.x
        return a, b

    def __len__(self):
        ln = math.sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)
        return ln

    def __contains__(self, p: Coordinate):
        a, b = self.coeffs
        inx = min(self.p1.x, self.p2.x) <= p.x <= max(self.p1.x, self.p2.x)
        iny = min(self.p1.y, self.p2.y) <= p.y <= max(self.p1.y, self.p2.y)
        aligned = a * p.x + b == p.y
        return inx and iny and aligned


class Polygon:
    def __init__(self, edges: List[LineSegment]):
        self._edges = tuple(edges)

        # Construct vertex list from edges
        self._vertices = set()  # Prevent duplicates
        for e in self._edges:
            self._vertices.add(e.p1)
            self._vertices.add(e.p2)
        self._vertices = tuple(self._vertices)

        # Sanity check
        assert len(self._vertices) == len(self._edges)

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges


_GraphNode = namedtuple('Node', ['coord', 'w'])


class VisibilityGraph:
    def __init__(self, s: Coordinate, t: Coordinate, segments=None):
        self._s, self._t = s, t
        self._segments = [] if segments is None else segments
        self._edges = None
        self._vertices = None

    def construct_edge_list(self):
        if self.constructed:
            print('WARNING: Overriding existing edge list.', file=sys.stderr)

        self._vertices = set()
        for s in self._segments:
            self._vertices.add(s.p1)
            self._vertices.add(s.p2)
        self._vertices = list(self._vertices)

        self._edges = {}
        for v in self._vertices:
            self._edges[v] = []

        for s in self._segments:
            self._edges[s.p1].append(_GraphNode(coord=s.p2, w=len(s)))
            self._edges[s.p2].append(_GraphNode(coord=s.p1, w=len(s)))

    @property
    def segments(self):
        return self._segments

    @property
    def constructed(self):
        return self._edges is not None and self._vertices is not None

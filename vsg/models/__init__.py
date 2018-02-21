from typing import List, Tuple, Dict

import sys

from .line import *


class Polygon:
    def __init__(self, vertices: List[Point]):
        """
        Initialize a new Polygon from a list of Points. Polygons are immutable.
        :param vertices: A list of Point that describes how to construct the Polygon.
        """
        if vertices[0] == vertices[-1]:
            vertices = vertices[:-1]
        self._vertices = vertices

        # Construct edge list from vertices
        self._edges = []
        for prev, current in zip(vertices[:-1], vertices[1:]):
            self._edges.append(LineSegment(prev, current))
        self._edges.append(LineSegment(vertices[-1], vertices[0]))

    def __contains__(self, item):
        return item in self.edges or item in self.vertices

    @property
    def vertices(self) -> Tuple[Point, ...]:
        return tuple(self._vertices)

    @property
    def edges(self) -> Tuple[LineSegment, ...]:
        return tuple(self._edges)

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
    def segments(self) -> Tuple[LineSegment]:
        return tuple(self._segments)

    def add_segment(self, segment: LineSegment):
        """
        Adds a segment to the graph. No op if the segment is already in the graph.
        :param segment: A LineSegment
        """
        if segment not in self.segments:
            self._segments.append(segment)

    @property
    def constructed(self) -> bool:
        return self._adj is not None and self._vertices is not None

    @property
    def adjacent_list(self) -> Dict[Point, _AdjacentNode]:
        return self._adj

    @property
    def vertices(self) -> Tuple[Point]:
        return tuple(self._vertices)

    @property
    def start(self) -> Point:
        return self._s

    @property
    def end(self) -> Point:
        return self._t

from typing import List
from functools import total_ordering
from sortedcontainers import SortedList

from vsg.models import Point, Polygon, VisibilityGraph, LineSegment


@total_ordering
class _SweepEdge(LineSegment):
    def __init__(self, segment: LineSegment, origin: Point):
        super().__init__(segment.p1, segment.p2)
        self.origin = origin

    def __eq__(self, other: LineSegment):
        pass

    def __ne__(self, other: LineSegment):
        pass

    def __gt__(self, other: LineSegment):
        pass


class _EventSearchTree:
    def __init__(self, origin: Point, target=None):
        self.origin = origin
        self.target = target
        self.store = SortedList()




def rotational_plane_sweep(s: Point, t: Point, obstacles: List[Polygon],
                           verbose=False) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)

    # Add all obstacle edges to the graph
    for obs in obstacles:
        for e in obs.edges:
            graph.add_segment(e)

    return graph




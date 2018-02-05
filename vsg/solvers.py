from typing import List

from vsg.models import Coordinate, Polygon, VisibilityGraph, LineSegment


def rotational_plane_sweep(s: Coordinate, t: Coordinate, obstacles: List[Polygon]) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)
    return graph


def full_check(s: Coordinate, t: Coordinate, obstacles: List[Polygon]) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)
    return graph

from typing import List

from vsg.models import Point, Polygon, VisibilityGraph, HalfLine, LineSegment


def rotational_plane_sweep(s: Point, t: Point, obstacles: List[Polygon],
                           verbose=False) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)
    points = [s, t]

    # Add all obstacle edges to the graph
    for obs in obstacles:
        for e in obs.edges:
            graph.add_segment(e)
        for p in obs.vertices:
            if p not in points:
                points.append(p)

    for i, p in enumerate(points[:-1]):
        # Sort other points by positive-x angle and distance to p
        others = points[i+1:]
        others.sort(key=lambda x: LineSegment(p, x).length)
        others.sort(key=lambda x: HalfLine.from_points(p, x).angle)
        hlines = list(map(lambda x: HalfLine.from_points(p, x), others))

        # Construct search tree
        xline = HalfLine(p, 0.)

    return graph




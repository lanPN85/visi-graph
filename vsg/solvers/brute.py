from typing import List

from vsg.models import Point, Polygon, VisibilityGraph, LineSegment


def rotational_plane_sweep(s: Point, t: Point, obstacles: List[Polygon],
                           verbose=False) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)
    return graph


def brute_force(s: Point, t: Point, obstacles: List[Polygon],
                verbose=False) -> VisibilityGraph:
    graph = VisibilityGraph(s, t)

    # Get vertex list
    verts = [s, t]
    for obs in obstacles:
        verts.extend(obs.vertices)

    for i, v1 in enumerate(verts[:-1]):
        for j, v2 in enumerate(verts[i+1:]):
            if v1 == v2:
                continue
            segment = LineSegment(v1, v2)

            # Check for impact to each obstacle
            visible = True
            for obs in obstacles:
                if segment in obs:
                    break
                if v1 in obs and v2 in obs:
                    visible = False
                    if verbose:
                        print('  %s: POLYGON DIAGONAL' % segment)
                    break
                else:
                    impacts = obs.impact_points(segment)
                    if impacts is None:
                        continue
                    for ip in impacts:
                        if ip != v1 and ip != v2:
                            visible = False
                            if verbose:
                                print('  %s: POLYGON IMPACT' % segment)
                            break

            if visible:
                graph.add_segment(segment)
                if verbose:
                    print('  %s: VISIBLE' % segment)

    return graph

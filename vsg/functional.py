import numpy as np

from vsg.models import LineSegment, Polygon, Coordinate


def intersect_point(l1: LineSegment, l2: LineSegment):
    a1, b1, c1 = l1.coeffs
    a2, b2, c2 = l2.coeffs

    A = np.asarray([[a1, b1], [a2, b2]], dtype=np.float)
    b = np.asarray([[-c1], [-c2]], dtype=np.float)

    try:
        x = np.linalg.solve(A, b)
        x = np.around(x, 5)
    except np.linalg.LinAlgError:
        return None

    x1, x2 = x[0, 0], x[1, 0]
    p = Coordinate(x1, x2)

    return p if p in l1 and p in l2 else None


def impact_points(polygon: Polygon, segment: LineSegment):
    points = []
    for edge in polygon.edges:
        p = intersect_point(segment, edge)
        if p is not None:
            points.append(p)

    return points if len(points) > 0 else None

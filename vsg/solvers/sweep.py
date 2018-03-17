from typing import List


from vsg.models import Point, Polygon, VisibilityGraph, HalfLine, LineSegment
from vsg.solvers.tree import BalancedEdgeSearchTree
from vsg import functional


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
        others = points[:]
        others.remove(p)
        others.sort(key=lambda x: LineSegment(p, x).length)
        others.sort(key=lambda x: HalfLine.from_points(p, x).angle)

        # Construct search tree
        point2edge, point2poly = {}, {}
        point2edge[s] = []
        point2edge[t] = []
        xline = HalfLine(p, 0.)
        tree = BalancedEdgeSearchTree()
        vis = [False] * len(others)

        # Add intersecting edges along with their visit order to the search tree
        tobs = None
        for obs in obstacles:
            if p in obs.vertices:
                tobs = obs

            for e in obs.edges:
                # Map vertices to their edges
                for v in (e.p1, e.p2):
                    point2poly[v] = obs
                    if v not in point2edge.keys():
                        point2edge[v] = [e]
                    else:
                        point2edge[v].append(e)

                ips = functional.hl_intersect_point(xline, e)
                if ips is not None and len(ips) > 1:
                    tree.add_node(e, VisitOrder(p, e))

        if tobs is not None:
            for j, op in enumerate(others):
                if op in tobs.vertices:
                    vis[j] = True

        # Find visible vertices
        print(p)
        for j, op in enumerate(others):
            if _visible(p, op, tree, point2poly, others, vis, j):
                graph.add_segment(LineSegment(p, op))
                vis[j] = True

            # Decide whether to insert or delete each edge
            baseline = VisitOrder(p, LineSegment(p, op))
            for e in point2edge[op]:
                _order = VisitOrder(p, e)
                if _order > baseline:
                    tree.add_node(e, _order)
                else:
                    tree.delete_node(e, _order)

    return graph


def _visible(origin: Point, p: Point, tree: BalancedEdgeSearchTree,
             point2poly: dict, others: list, vis: list, idx: int):
    pw = LineSegment(origin, p)
    try:
        it1 = functional.impact_points(point2poly[p], pw)
        if it1 is not None and len(it1) > 1:
            return False
    except KeyError:
        pass

    if idx == 0 or others[idx-1] not in pw:
        e = tree.leftmost()
        if e is not None and functional.intersect_point(pw, e) is not None:
            return False
        else:
            return True
    elif not vis[idx-1]:
        return False
    else:
        ww = LineSegment(p, others[idx - 1])
        it2 = tree.intersect_edge(ww, VisitOrder(origin, ww))
        if it2 is not None:
            return False
        else:
            return True


class VisitOrder:
    def __init__(self, origin: Point, line: LineSegment):
        self._origin = origin
        self._line = line
        if origin not in line:
            self.__calculate()
        else:
            other = line.p1 if line.p1 != origin else line.p2
            self._min_angle = HalfLine.from_points(origin, other).angle
            self._min_dist = LineSegment(origin, other).length

    def __calculate(self):
        hl1 = HalfLine.from_points(self._origin, self._line.p1)
        hl2 = HalfLine.from_points(self._origin, self._line.p2)
        self._min_angle = min(hl1.angle, hl2.angle)

        if hl1.angle < hl2.angle:
            _l = LineSegment(self._origin, self._line.p1)
        else:
            _l = LineSegment(self._origin, self._line.p2)
        self._min_dist = _l.length

    @property
    def min_angle(self):
        return self._min_angle

    @property
    def min_dist(self):
        return self._min_dist

    def __eq__(self, other):
        return self.min_angle == other.min_angle and\
               self.min_dist == other.min_dist

    def __ne__(self, other):
        return self.min_angle != other.min_angle or\
               self.min_dist != other.min_dist

    def __gt__(self, other):
        if self.min_angle == other.min_angle:
            return self.min_dist > other.min_dist
        else:
            return self.min_angle > other.min_angle

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        if self.min_angle == other.min_angle:
            return self.min_dist < other.min_dist
        else:
            return self.min_angle < other.min_angle

    def __le__(self, other):
        return self < other or self == other

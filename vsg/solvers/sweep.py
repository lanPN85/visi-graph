from typing import List
from sortedcontainers import SortedListWithKey


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
        # tree = BalancedEdgeSearchTree()
        tree = SortedListWithKey(key=lambda x: VisitOrder(p, x))
        vis = [False for _ in range(len(others))]

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

                if p not in e:
                    ips = functional.hl_intersect_point(xline, e)
                    if ips is not None and len(ips) > 1:
                        # tree.add_node(e, VisitOrder(p, e))
                        tree.add(e)

        if tobs is not None:
            for j, op in enumerate(others):
                if op in tobs.vertices:
                    vis[j] = True

        # Find visible vertices
        print('# ', p)
        print(tree)
        for j, op in enumerate(others):
            print('## ', op)
            if _visible(p, op, tree, point2poly, others, vis, j):
                print('  VISIBLE')
                graph.add_segment(LineSegment(p, op))
                vis[j] = True
            else:
                vis[j] = False

            # Decide whether to insert or delete each edge
            for e in point2edge[op]:
                rp = list(filter(lambda x: x != op, [e.p1, e.p2]))[0]
                if rp == p:
                    continue

                baseline = HalfLine(p)
                its = functional.hl_intersect_point(baseline, e)
                a0 = HalfLine.from_points(p, op).angle
                a1 = HalfLine.from_points(p, rp).angle
                before = a1 < a0

                if before:
                    print('  Removing %s' % str(e))
                    # tree.delete_node(e, VisitOrder(p, e))
                    tree.discard(e)
                else:
                    print('  Adding %s' % str(e))
                    # tree.add_node(e, VisitOrder(p, e))
                    tree.add(e)

    return graph


def _visible(origin: Point, p: Point, tree: SortedListWithKey,
             point2poly: dict, others: list, vis: list, idx: int):
    pw = LineSegment(origin, p)
    try:
        it1 = functional.impact_points(point2poly[p], pw)
        print('  I1:', it1)
        if it1 is not None and len(it1) > 1:
            return False
    except KeyError:
        pass

    if idx == 0 or others[idx-1] not in pw:
        # e = tree.leftmost()
        e = tree[0] if len(tree) > 0 else None
        print('  E:', e)

        if e is not None:
            it3 = functional.intersect_point(pw, e)
            if it3 is not None and it3 != p:
                return False
            else:
                return True
        else:
            return True
    elif not vis[idx-1]:
        print('  Prev')
        return False
    else:
        ww = LineSegment(p, others[idx - 1])
        # it2 = tree.intersect_edge(ww, VisitOrder(origin, ww))
        it2 = intersect_binsearch(tree, ww)
        print('  I2:', it2)
        if it2 is not None:
            return False
        else:
            return True


def intersect_binsearch(tree: SortedListWithKey, edge: LineSegment):
    length = len(tree)
    mid = length // 2
    current = tree[mid]
    it = None

    while it is None and mid > 0:
        it = functional.intersect_point(current, edge)
        mid = mid // 2
        current = tree[mid]
    return it


class VisitOrder:
    def __init__(self, origin: Point, line: LineSegment):
        self._origin = origin
        self._line = line
        self.__calculate()

    def __calculate(self):
        baseline = HalfLine(self._origin)
        cp = functional.hl_intersect_point(baseline, self._line)
        if cp is not None:
            self._is_cut = True
            self._cut_dist = LineSegment(cp, self._origin).length
            self._min_angle = None
            self._min_dist = None
        else:
            self._is_cut = False
            self._cut_dist = None

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

    @property
    def is_cut(self):
        return self._is_cut

    @property
    def cut_dist(self):
        return self._cut_dist

    def __str__(self):
        if self.is_cut:
            return 'Order(CUT, dist=%.2f)' % self.cut_dist
        else:
            return 'Order(NOCUT, angle=%.2f, dist=%.2f)' % (self.min_angle, self.min_dist)

    def __eq__(self, other):
        return self._is_cut == other.is_cut and self._cut_dist == other.cut_dist and\
            self.min_angle == other.min_angle and self.min_dist == other.min_dist

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if self.is_cut:
            if other.is_cut:
                return self.cut_dist > other.cut_dist
            else:
                return True
        else:
            if other.is_cut:
                return False
            else:
                if self.min_angle > other.min_angle:
                    return True
                else:
                    return self.min_dist > other.min_dist

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        if self.is_cut:
            if other.is_cut:
                return self.cut_dist < other.cut_dist
            else:
                return False
        else:
            if other.is_cut:
                return True
            else:
                if self.min_angle < other.min_angle:
                    return True
                else:
                    return self.min_dist < other.min_dist

    def __le__(self, other):
        return self < other or self == other

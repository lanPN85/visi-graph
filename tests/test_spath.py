import unittest

from vsg import Point, LineSegment, VisibilityGraph

import vsg.spath as spath


class SpathTest(unittest.TestCase):
    def test_dijkstra_1(self):
        s = Point(0., 0.)
        t = Point(20., 11.)

        segments = [
            LineSegment(Point(0., 0.), Point(1., 3.)),
            LineSegment(Point(0., 0.), Point(5., 2.)),
            LineSegment(Point(0., 0.), Point(2., 1.)),
            LineSegment(Point(1., 3.), Point(2., 4.)),
            LineSegment(Point(2., 4.), Point(5., 2.)),
            LineSegment(Point(5., 2.), Point(2., 1.)),
            LineSegment(Point(2., 1.), Point(1., 3.)),
            LineSegment(Point(20., 11.), Point(5., 2.)),
            LineSegment(Point(20., 11.), Point(2., 4.))
        ]

        graph = VisibilityGraph(s, t, segments)
        path = spath.dijkstra(graph)
        correct = [
            Point(0., 0.), Point(5., 2.), Point(20., 11.)
        ]
        self.assertListEqual(correct, path)


if __name__ == '__main__':
    unittest.main()
import unittest

from vsg import Coordinate, LineSegment, VisibilityGraph

import vsg.spath as spath


class SpathTest(unittest.TestCase):
    def test_dijkstra_1(self):
        s = Coordinate(0., 0.)
        t = Coordinate(20., 11.)

        segments = [
            LineSegment(Coordinate(0., 0.), Coordinate(1., 3.)),
            LineSegment(Coordinate(0., 0.), Coordinate(5., 2.)),
            LineSegment(Coordinate(0., 0.), Coordinate(2., 1.)),
            LineSegment(Coordinate(1., 3.), Coordinate(2., 4.)),
            LineSegment(Coordinate(2., 4.), Coordinate(5., 2.)),
            LineSegment(Coordinate(5., 2.), Coordinate(2., 1.)),
            LineSegment(Coordinate(2., 1.), Coordinate(1., 3.)),
            LineSegment(Coordinate(20., 11.), Coordinate(5., 2.)),
            LineSegment(Coordinate(20., 11.), Coordinate(2., 4.))
        ]

        graph = VisibilityGraph(s, t, segments)
        path = spath.dijkstra(graph)
        correct = [
            Coordinate(0., 0.), Coordinate(5., 2.), Coordinate(20., 11.)
        ]
        self.assertListEqual(correct, path)


if __name__ == '__main__':
    unittest.main()
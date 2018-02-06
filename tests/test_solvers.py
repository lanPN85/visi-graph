import unittest

from vsg import Polygon, Point, LineSegment

import vsg.solvers as solvers


class SolverTest(unittest.TestCase):
    def test_brute_1(self):
        s = Point(0., 0.)
        t = Point(20., 11.)

        o1 = Polygon([
            Point(1., 3.), Point(2., 4.),
            Point(5., 2.), Point(2., 1.)
        ])

        graph = solvers.brute_force(s, t, [o1])
        correct = [
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

        self.assertEqual(len(graph.segments), len(correct))
        for s in graph.segments:
            self.assertIn(s, correct)


if __name__ == '__main__':
    unittest.main()

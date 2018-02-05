import unittest

from vsg import Polygon, Coordinate, LineSegment

import vsg.solvers as solvers


class SolverTest(unittest.TestCase):
    def test_brute_1(self):
        s = Coordinate(0., 0.)
        t = Coordinate(20., 11.)

        o1 = Polygon([
            LineSegment(Coordinate(1., 3.), Coordinate(2., 4.)),
            LineSegment(Coordinate(2., 4.), Coordinate(5., 2.)),
            LineSegment(Coordinate(5., 2.), Coordinate(2., 1.)),
            LineSegment(Coordinate(2., 1.), Coordinate(1., 3.))
        ])

        graph = solvers.brute_force(s, t, [o1])
        correct = [
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

        self.assertEqual(len(graph.segments), len(correct))
        for s in graph.segments:
            self.assertIn(s, correct)


if __name__ == '__main__':
    unittest.main()

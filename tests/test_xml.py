import unittest
import os

import vsg.fileio.results as results

from vsg import Point, VisibilityGraph, LineSegment


class XmlTest(unittest.TestCase):
    def test_path_xml(self):
        path = [Point(1, 2), Point(3, 4), Point(5, 6)]
        results.path_to_xml(path, 'sp_test.xml')
        path2 = results.path_from_xml('sp_test.xml')
        self.assertListEqual(path, path2)

    def test_graph_xml(self):
        graph = VisibilityGraph(Point(0., 0.), Point(20., 11.), [
            LineSegment(Point(0., 0.), Point(1., 3.)),
            LineSegment(Point(0., 0.), Point(5., 2.)),
            LineSegment(Point(0., 0.), Point(2., 1.)),
            LineSegment(Point(1., 3.), Point(2., 4.)),
            LineSegment(Point(2., 4.), Point(5., 2.)),
            LineSegment(Point(5., 2.), Point(2., 1.)),
            LineSegment(Point(2., 1.), Point(1., 3.)),
            LineSegment(Point(20., 11.), Point(5., 2.)),
            LineSegment(Point(20., 11.), Point(2., 4.))
        ])
        results.graph_to_xml(graph, 'vg_test.xml')
        graph2 = results.graph_from_xml('vg_test.xml')

        self.assertEqual(graph2.start, graph.start)
        self.assertEqual(graph2.end, graph.end)
        self.assertEqual(len(graph2.segments), len(graph.segments))
        for s in graph2.segments:
            self.assertIn(s, graph.segments)

    @classmethod
    def tearDownClass(cls):
        os.remove('sp_test.xml')
        os.remove('vg_test.xml')


if __name__ == '__main__':
    unittest.main()

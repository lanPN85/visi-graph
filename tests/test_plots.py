import sys
sys.path.append('.')
import matplotlib.pyplot as plt

from vsg import Coordinate, Polygon, LineSegment

import vsg.plots as plots
import vsg.solvers as solvers
import vsg.spath as spath


if __name__ == '__main__':
    # plt.xkcd()
    s = Coordinate(0., 0.)
    t = Coordinate(11., 11.)

    o1 = Polygon([
        LineSegment(Coordinate(1., 3.), Coordinate(2., 4.)),
        LineSegment(Coordinate(2., 4.), Coordinate(5., 2.)),
        LineSegment(Coordinate(5., 2.), Coordinate(2., 1.)),
        LineSegment(Coordinate(2., 1.), Coordinate(1., 3.))
    ])

    o2 = Polygon([
        LineSegment(Coordinate(4., 8.), Coordinate(7., 8.)),
        LineSegment(Coordinate(7., 8.), Coordinate(4.7, 5.4)),
        LineSegment(Coordinate(4.7, 5.4), Coordinate(4., 8.))
    ])

    obs = [o1, o2]

    graph = solvers.brute_force(s, t, obs)

    fig = plt.figure()
    ax1 = fig.add_subplot(131)
    ax1.set_title('Initial state')
    plots.plot_initial_state(s, t, obs, ax1)
    # fig.legend(loc='lower center', ncol=2)
    ax1.legend()

    ax2 = fig.add_subplot(132)
    ax2.set_title('Visibility graph')
    plots.plot_visi_graph(graph, ax2, obstacles=obs)
    ax2.legend()

    ax3 = fig.add_subplot(133)
    ax3.set_title('Shortest path')
    path = spath.dijkstra(graph)
    plots.plot_shortest_path(path, ax3, obstacles=obs)
    ax3.legend()

    fig.show()
    input()

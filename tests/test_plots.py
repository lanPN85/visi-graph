import sys
sys.path.append('.')
import matplotlib.pyplot as plt

from vsg import Point, Polygon, LineSegment

import vsg.plots as plots
import vsg.solvers as solvers
import vsg.spath as spath


if __name__ == '__main__':
    # plt.xkcd()
    s = Point(0., 0.)
    t = Point(11., 11.)

    o1 = Polygon([
        Point(1., 3.),
        Point(2., 4.),
        Point(5., 2.),
        Point(2., 1.)
    ])

    o2 = Polygon([
        Point(4., 8.),
        Point(7., 8.),
        Point(4.7, 5.4)
    ])

    obs = [o1, o2]

    graph = solvers.brute_force(s, t, obs, verbose=True)

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

    fig.savefig('test_fig.png')

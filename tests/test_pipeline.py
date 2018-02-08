import sys
sys.path.append('.')
import matplotlib.pyplot as plt

import vsg.fileio.plots as plots
import vsg.solvers as solvers
import vsg.spath as spath
import vsg.fileio.ggb as ggb


if __name__ == '__main__':
    s, t, obs = ggb.config_from_ggb('../data/ggb/vg-1.ggb')

    graph = solvers.brute_force(s, t, obs)

    fig = plt.figure(dpi=300)
    ax1 = fig.add_subplot(131)
    ax1.set_title('Initial state')
    plots.plot_initial_state(s, t, obs, ax1)
    # fig.legend(loc='lower center', ncol=2)

    ax2 = fig.add_subplot(132)
    ax2.set_title('Visibility graph')
    plots.plot_visi_graph(graph, ax2, obstacles=obs)

    ax3 = fig.add_subplot(133)
    ax3.set_title('Shortest path')
    path = spath.dijkstra(graph)
    plots.plot_shortest_path(path, ax3, obstacles=obs)

    fig.savefig('test_fig.png')

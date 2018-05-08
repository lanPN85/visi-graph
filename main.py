from argparse import ArgumentParser

import os
import datetime as dt
import matplotlib.pyplot as plt

import vsg
import vsg.fileio as fileio

SOLVERS = {
    'brute': vsg.brute_force,
    'sweep': vsg.rotational_plane_sweep
}
SPATHS = {
    'dijkstra': vsg.dijkstra
}


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('--input', '-i', required=True,
                        help='Path to input file or folder')
    parser.add_argument('--output', '-o', default='out/',
                        help='Folder to store results')
    parser.add_argument('--solver', '-s', default='brute',
                        help='Solver algorithm to use. Choices: %s. Defaults to `brute`.' % SOLVERS.keys())
    parser.add_argument('--spath', '-sp', default='dijkstra',
                        help='Shortest path algorithm to use. Choices: %s. Defaults to `dijkstra`' % SPATHS.keys())
    parser.add_argument('--dpi', type=int, default=200,
                        help='DPI quality of output images. Defaults to 200')
    parser.add_argument('--verbose', '-v', action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    os.makedirs(args.output, exist_ok=True)

    # Get list of input files
    if os.path.isdir(args.input):
        files = os.listdir(args.input)
        files = list(map(lambda f: os.path.join(args.input, f), files))
    else:
        files = [args.input]

    # Parameter check
    if args.solver not in SOLVERS:
        raise ValueError('Invalid solver %s.' % args.solver)
    if args.spath not in SPATHS:
        raise ValueError('Invalid shortest path %s.' % args.spath)

    fig = plt.figure(dpi=args.dpi)

    for fn in files:
        print('Reading %s ...' % fn)
        s, t, obs = fileio.ggb.config_from_ggb(fn)

        _st = dt.datetime.now()
        print('Constructing graph...')
        graph = SOLVERS[args.solver](s, t, obs, verbose=args.verbose)
        _el = (dt.datetime.now() - _st).microseconds // 1000
        print('[Time: %dms]' % _el)

        _st = dt.datetime.now()
        print('Finding shortest path...')
        path = SPATHS[args.spath](graph)
        _el = (dt.datetime.now() - _st).microseconds // 1000
        print('[Time: %dms]' % _el)

        print('Storing results to %s' % args.output)
        prefix = str(os.path.split(fn)[1].split('.')[0])
        fileio.path_to_xml(path, os.path.join(args.output, prefix + '.path.xml'))
        fileio.graph_to_xml(graph, os.path.join(args.output, prefix + '.graph.xml'))

        # Generates and saves figure
        ax1 = fig.add_subplot(131)
        ax1.set_title('Initial state')
        fileio.plots.plot_initial_state(s, t, obs, ax1)

        ax2 = fig.add_subplot(132)
        ax2.set_title('Visibility graph')
        fileio.plots.plot_visi_graph(graph, ax2, obstacles=obs)

        ax3 = fig.add_subplot(133)
        ax3.set_title('Shortest path')
        fileio.plots.plot_shortest_path(path, ax3, obstacles=obs)
        plt.tight_layout()

        fig.savefig(os.path.join(args.output, prefix + '.png'))
        fig.clf()

        print('Done.')
        print()

from argparse import ArgumentParser

import os

import vsg

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
    parser.add_argument('--output', '-o', default='out',
                        help='Folder to store results')
    parser.add_argument('--solver', '-s', default='brute',
                        help='Solver algorithm to use. Choices: [brute]. Defaults to `brute`.')
    parser.add_argument('--spath', '-sp', default='dijkstra',
                        help='Shortest path algorithm to use. Choices: [dijkstra]. Defaults to `dijkstra`')
    parser.add_argument('--dpi', type=int, default=100,
                        help='DPI quality of output images. Defaults to 100')
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

    for fn in files:
        print('Reading %s ...' % fn)
        s, t, obs = vsg.inp.config_from_ggb(fn)

        print('Constructing graph...')
        graph = SOLVERS[args.solver](s, t, obs, verbose=args.verbose)

        print('Finding shortest path')
        path = SPATHS[args.spath](graph)

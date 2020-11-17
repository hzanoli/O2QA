import argparse

import o2qaplots.plot as plot
import o2qaplots.compare as compare


def cli():
    """Main entrypoint of the program. It redirects the input to the correct function."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True, help='Action to be performed')

    plot_parser = subparsers.add_parser('plot', description=plot.parser_description)
    plot.add_parser_options(plot_parser)

    compare_parser = subparsers.add_parser('compare', description=compare.parser_description)
    compare.add_parser_options(compare_parser)
    args = parser.parse_args()

    if args.command == 'plot':
        plot.plot(args)
    elif args.command == 'compare':
        compare.compare(args)

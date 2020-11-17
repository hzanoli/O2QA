import argparse

import o2qaplots.plot as plot
import o2qaplots.compare as compare


def cli():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    plot_parser = subparsers.add_parser('plot', description=plot.parser_description)
    plot.add_parser_options(plot_parser)

    compare_parser = subparsers.add_parser('compare', description=compare.parser_description)
    compare.add_parser_options(compare_parser)
    args = parser.parse_args()

    print(args)

    plot.plot(args)



import argparse

import ROOT

from o2qaplots.plot import discover_histograms, plot_1d, plot_profile, get_histogram, save

parser_description = 'Compare the results of two files'


def compare_histograms(file_name_a, file_name_b, output_dir, normalize, label_legend, ratio):
    histograms_info = discover_histograms(file_name_a)

    histograms_a = {h: get_histogram(file_name_a, h.path, h.name) for h in histograms_info}
    histograms_b = {h: get_histogram(file_name_b, h.path, h.name) for h in histograms_info}

    histograms_1d_keys = [x for x in histograms_a.keys() if x.root_class.startswith('TH1')]
    histograms_2d_keys = [x for x in histograms_a.keys() if x.root_class.startswith('TH2')]

    colors = [ROOT.kMagenta, ROOT.kBlue]

    plot_hist_1d = {info: plot_1d([histograms_a[info], histograms_b[info]], normalize=normalize, labels=label_legend,
                                  colors=colors, plot_errors=False, plot_ratio=False) for info in histograms_1d_keys}

    plot_hist_2d_profile = {info: plot_profile(histograms_a[info], histograms_b[info], axis='x',
                                               labels=label_legend, colors=colors, plot_errors=True, plot_ratio=False)
                            for info in histograms_2d_keys}

    for info, canvas in plot_hist_1d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d_profile.items():
        save(info, canvas, output_dir, '_profile')


def compare(args):
    plot_ratio = not args.no_ratio
    compare_histograms(args.file1, args.file2, args.output, args.normalize, (args.label1, args.label2), plot_ratio)


def add_parser_options(parser):
    parser.add_argument('file1', help='Location of the analysis results file to be plotted')
    parser.add_argument('file2', help='Location of the analysis results file to be plotted')
    parser.add_argument('--label1', '-l1', help='Label for histograms in file1', default='Run5')
    parser.add_argument('--label2', '-l2', help='Label for histograms in file2', default='Run2')
    parser.add_argument('--output', '-o', help='Location to save the produced files', default="qa_output")
    parser.add_argument('--normalize', '-n', help='Normalize by the integral.', action='store_true', default=False)
    parser.add_argument('--no_ratio', '-nr', help='Do not plot the ratio plot.', action='store_true', default=False)


if __name__ == '__main__':

    parser_main = argparse.ArgumentParser(description=parser_description)
    add_parser_options(parser_main)
    args_main = parser_main.parse_args()

    compare(args_main)

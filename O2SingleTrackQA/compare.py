import argparse
import os
import ROOT

from plot import discover_histograms, discover_categories, plot_1d, plot_profile, get_histogram, save


def compare_histograms(file_name_1, file_name_2, output_dir, normalize):
    histograms_info = discover_histograms(file_name_1)

    # Create output folders
    os.makedirs(output_dir, exist_ok=True)

    for category in discover_categories(file_name_1):
        os.makedirs(output_dir + "/" + category, exist_ok=True)

    histograms_1 = {h: get_histogram(file_name_1, h.category, h.name) for h in histograms_info}
    histograms_2 = {h: get_histogram(file_name_2, h.category, h.name) for h in histograms_info}

    histograms_1d_keys = [x for x in histograms_1.keys() if x.root_class.startswith('TH1')]
    histograms_2d_keys = [x for x in histograms_1.keys() if x.root_class.startswith('TH2')]

    label_legend = ['Run5', 'Run2']
    colors = [ROOT.kMagenta, ROOT.kBlue]

    plot_hist_1d = {info: plot_1d([histograms_1[info], histograms_2[info]], normalize=normalize, labels=label_legend,
                                  colors=colors, draw_option='HIST') for info in histograms_1d_keys}

    plot_hist_2d_profile = {info: plot_profile(histograms_1[info], histograms_2[info], axis='x', labels=label_legend,
                                               colors=colors)
                            for info in histograms_2d_keys}

    for info, canvas in plot_hist_1d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d_profile.items():
        save(info, canvas, output_dir, '_profile')


def compare():
    parser = argparse.ArgumentParser('Compare the results of two files of the single QA')
    parser.add_argument('file1', help='Location of the analysis results file to be plotted')
    parser.add_argument('file2', help='Location of the analysis results file to be plotted')
    parser.add_argument('--output', '-o', help='Location to save the produced files',
                        default="qa_output")
    parser.add_argument('--normalize', '-n', help='Normalize histograms by the integral.', action='store_true',
                        default=False)
    args = parser.parse_args()
    compare_histograms(args.file1, args.file2, args.output, args.normalize)


if __name__ == '__main__':
    compare()

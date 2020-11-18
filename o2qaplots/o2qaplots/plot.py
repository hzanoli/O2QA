import argparse
import os
import os.path
import pathlib

from o2qaplots.file_utils import discover_histograms, HistogramInfo
from o2qaplots.plot_mpl import plot_1d_mpl
from o2qaplots.plot_root import plot_1d_root, profile_histogram_root

from o2qaplots.config import JsonConfig, PlotConfig

parser_description = 'Plots all the histogram from a file into PDF.'


def get_histogram(input_file, sub_folders, histogram_name, backend='root'):
    """ Reads an histogram located in input_file. It must be in a ROOT.TDirectory called category_folder and be called
    histogram_name.

    Args:
        input_file: the name of the ROOT file with the histogram.
        sub_folders: the chain of ROOT.TDirectory that the histogram is in.
        histogram_name: name of the histogram in the folder.
        backend: if 'root', the histogram will be read using ROOT. If 'python', uproot will be used.
    Returns:
        The histogram pointed. The type of the object depends on the chosen backend.
    """
    if backend == 'root':
        import ROOT
        ROOT.TH1.AddDirectory(False)
        file = ROOT.TFile(input_file)

        folder = file
        for sub_folder in sub_folders:
            if sub_folder is not None:
                folder = folder.Get(sub_folder)

        return folder.Get(histogram_name).Clone()
    else:
        import uproot as up
        return up.open(input_file)['/'.join(sub_folders) + '/' + histogram_name]


def _validate_size(histograms, attribute):
    """Checks if histograms and attributes have the same size."""
    if attribute is not None:
        if len(histograms) != len(attribute):
            raise ValueError("The size of the lists do not match the number of histograms.")


def plot_1d(histograms_to_plot, normalize=False, plot_errors=True, backend='root', labels=None, colors=None,
            draw_option='', plot_ratio=False, plot_config: PlotConfig=None):
    """Plot a list of histograms to a ROOT.Canvas or matplotlib.Axes.

    Args:
        *histograms_to_plot: the histograms to be plotted.
        draw_option: if backend='root', this will be passed to the Draw method of the histogram. If backend='python, you
            should provide a dict which will be passed as kwargs for matplotlib.
        normalize: whether the histograms should be normalized or not.
        labels: The labels to be used in the legend.
        colors: The colors for each histogram.
        plot_errors: if true, the uncertainties in x and y will be plotted. Otherwise the plot will use a only a line.
        backend: if 'root', the histogram will be plotted using ROOT. If 'python', matplotlib will be used.

    Returns:
        A list with  ROOT.Canvas or matplotlib.Axes with the histograms drawn.
    """
    if len(histograms_to_plot) == 0:
        return []

    _validate_size(histograms_to_plot, labels)
    _validate_size(histograms_to_plot, colors)

    if backend == 'root':
        return plot_1d_root(histograms_to_plot, draw_option, labels, colors, normalize, plot_errors, plot_ratio,
                            plot_config.x_axis.view_range, plot_config.y_axis.view_range, plot_config.x_axis.log,
                            plot_config.y_axis.log)
    elif backend == 'python':
        return plot_1d_mpl(histograms_to_plot, draw_option, labels, colors, normalize, plot_errors)


def plot_2d(histogram, draw_option='colz1'):
    """Plot a list of histograms to a canvas. """
    import ROOT
    canvas = ROOT.TCanvas()
    canvas.cd()
    histogram.Draw(draw_option)
    return canvas


def profile_histogram(histogram, axis):
    """Make a profile (taking mean of each bin) of histogram in de designated axis."""
    profile = profile_histogram_root(axis, histogram)

    return profile


def plot_profile(*histograms, draw_option='', axis='x', **kwargs):
    """Plot a profile histogram, taking the average of each bin"""
    profiles = [profile_histogram(h, axis) for h in histograms]
    return plot_1d(profiles, draw_option=draw_option, **kwargs)


def save(info: HistogramInfo, canvas_or_ax, base_output_dir, suffix=''):
    """Save a ROOT.TCanvas or a matplotplib Axes into an pdf file."""

    output_file = base_output_dir + '/' + '/'.join(info.path) + '/' + info.name + suffix + '.pdf'

    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    try:
        canvas_or_ax.SaveAs(output_file)
    except AttributeError:
        canvas_or_ax.get_figure().savefig(output_file, bbox_inches='tight')

    _check_file_saved(output_file)


def _check_file_saved(file):
    """Checks if file exists.

    Raises:
        FileNotFoundError is file does not exist.
    """
    file_path = pathlib.Path(file)
    if not file_path.is_file():
        raise FileNotFoundError("It was not possible to save the file: " + file)


def plot_histograms(file_name, output_dir, normalize, backend,
                    plot_config_file=os.path.dirname(os.path.abspath(__file__)) + '/config/qa_plot_default.json'):
    json_config = JsonConfig(plot_config_file)
    histograms_info = discover_histograms(file_name)

    histograms = {h: get_histogram(file_name, h.path, h.name, backend) for h in histograms_info}
    histograms_1d_keys = [x for x in histograms.keys() if x.root_class.startswith('TH1')]
    histograms_2d_keys = [x for x in histograms.keys() if x.root_class.startswith('TH2')]

    plot_hist_1d = {info: plot_1d([histograms[info]], normalize, False, backend, plot_config=json_config.get(info.name))
                    for info in histograms_1d_keys}

    plot_hist_2d = {info: plot_2d(histograms[info]) for info in histograms_2d_keys}

    plot_hist_2d_profile = {info: plot_profile(histograms[info], axis='x', plot_config=json_config.get(info.name))
                            for info in histograms_2d_keys}

    for info, canvas in plot_hist_1d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d_profile.items():
        save(info, canvas, output_dir, '_profile')


def plot(args=None):
    """Entrypoint function to parse the arguments and make plots of single datasets. """
    if args is None:
        main_parser = argparse.ArgumentParser(description=parser_description)
        add_parser_options(main_parser)
        args = main_parser.parse_args()

    backend_ = 'root'
    if args.python:
        backend_ = 'python'

    plot_histograms(args.file, args.output, args.normalize, backend_)


def add_parser_options(parser):
    parser.add_argument('file', help='Location of the analysis results file to be plotted')
    parser.add_argument('--output', '-o',
                        help='Location to save the produced files',
                        default="qa_output")
    parser.add_argument('--normalize', '-n', help='Normalize histograms by the integral.',
                        action='store_true',
                        default=False)
    parser.add_argument('--python', '-p', help='Use the pure python interface instead of ROOT (in test).',
                        action='store_true',
                        default=False)


if __name__ == '__main__':
    plot()

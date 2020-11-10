import argparse
import os
import pathlib

from file_utils import discover_histograms, discover_categories
from plot_mpl import plot_1d_mpl
from plot_root import plot_1d_root, profile_histogram_root


def get_histogram(input_file, category_folder, histogram_name, backend='root'):
    """ Reads an histogram located in input_file. It must be in a ROOT.TDirectory called category_folder and be called
    histogram_name.

    Args:
        input_file: the name of the ROOT file with the histogram.
        category_folder: the ROOT.TDirectory that the histogram is in.
        histogram_name: name of the histogram in the folder.
        backend: if 'root', the histogram will be read using ROOT. If 'python', uproot will be used.
    Returns:
        The histogram pointed. The type of the object depends on the chosen backend.
    """
    if backend == 'root':
        import ROOT
        ROOT.TH1.AddDirectory(False)
        file = ROOT.TFile(input_file)
        return file.Get(category_folder).Get(histogram_name).Clone()
    else:
        import uproot as up
        return up.open(input_file)[category_folder + '/' + histogram_name]


def _validate_size(histograms, attribute):
    """Checks if histograms and attributes have the same size."""
    if attribute is not None:
        if len(histograms) != len(attribute):
            raise ValueError("The size of the lists do not match the number of histograms.")


def plot_1d(histograms_to_plot, normalize=False, plot_errors=True, backend='root', labels=None, colors=None,
            draw_option=''):
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
        return plot_1d_root(histograms_to_plot, draw_option, labels, colors, normalize, plot_errors)
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


def save(info, canvas_or_ax, output_directory, suffix=''):
    """Save a ROOT.TCanvas or a matplotplib Axes into an pdf file."""
    output_file = output_directory + "/" + info.category + "/" + info.name + suffix + '.pdf'

    try:
        canvas_or_ax.SaveAs(output_file)
    except AttributeError:
        canvas_or_ax.get_figure().savefig(output_file, bbox_inches='tight')

    _check_file_saved(output_file)


def _check_file_saved(file):
    file_path = pathlib.Path(file)
    if not file_path.is_file():
        raise RuntimeError("It was not possible to save the file: " + file)


def plot_histograms(file_name, output_dir, normalize, backend):
    histograms_info = discover_histograms(file_name)

    # Create output folders
    os.makedirs(output_dir, exist_ok=True)

    for category in discover_categories(file_name):
        os.makedirs(output_dir + "/" + category, exist_ok=True)

    histograms = {h: get_histogram(file_name, h.category, h.name, backend) for h in histograms_info}
    histograms_1d_keys = [x for x in histograms.keys() if x.root_class.startswith('TH1')]
    histograms_2d_keys = [x for x in histograms.keys() if x.root_class.startswith('TH2')]

    plot_hist_1d = {info: plot_1d([histograms[info]], normalize, False, backend)
                    for info in histograms_1d_keys}

    plot_hist_2d = {info: plot_2d(histograms[info]) for info in histograms_2d_keys}

    plot_hist_2d_profile = {info: plot_profile(histograms[info], axis='x') for info in histograms_2d_keys}

    for info, canvas in plot_hist_1d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d.items():
        save(info, canvas, output_dir)

    for info, canvas in plot_hist_2d_profile.items():
        save(info, canvas, output_dir, '_profile')


def plot():
    """Entrypoint function to parse the arguments and make plots of single datasets. """
    parser = argparse.ArgumentParser('Plotting for the single-track QA for O2')
    parser.add_argument('file', help='Location of the analysis results file to be plotted')
    parser.add_argument('--output', '-o',
                        help='Location to save the produced files',
                        default="qa_output")
    parser.add_argument('--normalize', '-n', help='Normalize histograms by the integral.',
                        action='store_true',
                        default=False)
    parser.add_argument('--python', '-p', help='Use the pure python interface instead of ROOT.',
                        action='store_true',
                        default=False)

    args = parser.parse_args()
    backend_ = 'root'

    if args.python:
        backend_ = 'python'

    plot_histograms(args.file, args.output, args.normalize, backend_)


if __name__ == '__main__':
    plot()

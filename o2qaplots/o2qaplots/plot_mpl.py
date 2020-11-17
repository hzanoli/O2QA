import numpy as np


def plot_1d_mpl(histograms_to_plot, draw_option, labels=None, colors=None, normalize=False, plot_errors=False):
    """ Plots an histogram from ROOT using matplotlib
    Args:
        histograms_to_plot: histogram object, read by uproot, to be plotted.
        draw_option: dict to be passed as kwargs to matplotlib.
        labels: list with the label for each histogram.
        colors: list with the colors for each histogram. If none, the automatic pallet is used.
        normalize: If true, the histogram is normalized by 1./sum(counts * bins_width).
        plot_errors: whether to plot or not the uncertainties in x and y/
    Returns:
        ax: the Axes with the all the plotted histograms.
    """
    if labels is None:
        labels = [None for _ in range(len(histograms_to_plot))]
    if colors is None:
        colors = [None for _ in range(len(histograms_to_plot))]

    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    fig, ax = plt.subplots()

    for hist, label, color in zip(histograms_to_plot, labels, colors):
        _plot_histogram_1d_mpl(hist, ax, label, color, normalize, plot_errors, **draw_option)
        ax.set_xlabel(hist._fXaxis._fTitle.decode())
        ax.set_ylabel(hist._fYaxis._fTitle.decode())

    return ax


def _plot_histogram_1d_mpl(histogram, ax, label, color, normalize, plot_errors, **kwargs):
    bins = np.array(histogram.edges)
    histogram_df = histogram.pandas()

    x_mid = (bins[:-1] + bins[1:]) / 2.
    x_error = np.diff(bins)/2.

    counts = histogram_df['count'].values[1:-1]
    counts_error = np.sqrt(histogram_df['variance']).values[1:-1]

    if plot_errors:
        if normalize:
            counts = counts * 1./sum(counts * np.diff(bins))
        ax.errorbar(x_mid, counts, counts_error, x_error, **kwargs)
    else:
        ax.hist(x_mid, bins=bins, weights=counts, label=label, color=color, density=normalize, histtype='step',
                **kwargs)
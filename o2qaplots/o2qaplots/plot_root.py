def _set_root_global_style():
    """Set the global style for the plots"""
    import ROOT
    ROOT.gROOT.ForceStyle(True)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gROOT.SetStyle('ATLAS')


def plot_1d_root(histograms_to_plot, draw_option='', labels=None, colors=None, normalize=False,
                 plot_errors=False, plot_ratio=False):
    """ Plots an histogram from ROOT using ROOT.
    Args:
        histograms_to_plot: histogram object, read by ROOT, to be plotted.
        draw_option: draw option to be passed to the ROOT Draw function.
        labels: list with the label for each histogram.
        colors: list with the colors for each histogram. If none, the automatic pallet is used.
        normalize: If true, the histogram is normalized by 1./sum(counts * bins_width).
        plot_errors: whether to plot or not the uncertainties in x and y
        plot_ratio: Works only for 2 histograms. If true, a ratio between the two plots is included.
    Returns:
        ax: the Axes with the all the plotted histograms.
    """
    import ROOT

    if plot_ratio and len(histograms_to_plot) != 2:
        raise ValueError("Ratio plots can only be used if two histograms are passed.")

    _prepare_root_histograms(colors, histograms_to_plot, labels, normalize)

    common_draw_opt = ""
    if colors is None:
        common_draw_opt += "PLC PMC"

    canvas = ROOT.TCanvas()
    canvas.cd()

    if not plot_errors:
        common_draw_opt += 'HIST'

    if plot_ratio:
        ratio_plot = ROOT.TRatioPlot(histograms_to_plot[0], histograms_to_plot[1])
        ratio_plot.Draw()
    else:
        histograms_to_plot[0].Draw(draw_option + common_draw_opt)

        for h in histograms_to_plot[1:]:
            h.Draw(draw_option + "SAME" + common_draw_opt)

    if labels is not None:
        legend = canvas.BuildLegend()
        legend.SetLineWidth(0)
        legend.SetBorderSize(0)

    return canvas


def _prepare_root_histograms(colors, histograms_to_plot, labels, normalize):
    _set_root_global_style()
    if normalize:
        normalize_histograms(histograms_to_plot)
    max_value, min_value = _get_histogram_ranges(histograms_to_plot)
    for h in histograms_to_plot:
        h.GetYaxis().SetRangeUser(min_value, 1.1 * max_value)
    if labels is not None:
        for h, label in zip(histograms_to_plot, labels):
            h.SetTitle(label)
    if colors is not None:
        for h, color in zip(histograms_to_plot, colors):
            h.SetLineColor(color)
            h.SetMarkerColor(color)


def _get_histogram_ranges(histograms_to_plot):
    max_value = max([h.GetMaximum() for h in histograms_to_plot])
    min_value = min([h.GetMinimum() for h in histograms_to_plot] + [0])
    return max_value, min_value


def normalize_histograms(histograms_to_plot):
    for h in histograms_to_plot:
        h.GetYaxis().SetTitle('Relative Frequency')
        h.Scale(1. / h.Integral())
        if h.GetXaxis().GetTitle() == 'Track Multiplicity':
            h.GetXaxis().SetRangeUser(0, 250)


def profile_histogram_root(axis, h):
    if axis.lower() == 'x':
        profile = h.ProfileX()
        profile.GetYaxis().SetTitle('< ' + h.GetYaxis().GetTitle() + ' >')
    else:
        profile = h.ProfileY()
        profile.GetXaxis().SetTitle('< ' + h.GetXaxis().GetTitle() + ' >')
    return profile
import ROOT
from collections import namedtuple

Histogram = namedtuple('Histogram', ['category', 'name', 'root_class'])


def discover_histograms(file_name):
    """Discovers the histograms saved in a file with multiple TDirectories.

    Args:
        file_name: the file to be inspected.

    Returns
        histograms: a dictionary with {folder: {type: [histogram_name, ] }]}
    """
    file = ROOT.TFile(file_name)
    file_iterator = ROOT.TIter(file.GetListOfKeys())
    histograms = list()

    for category_key in file_iterator:
        category = file.Get(category_key.GetName())
        for histogram in ROOT.TIter(category.GetListOfKeys()):
            histograms.append(Histogram(category_key.GetName(), histogram.GetName(), histogram.GetClassName()))

    return histograms

def discover_categories(file_name):
    file = ROOT.TFile(file_name)
    file_iterator = ROOT.TIter(file.GetListOfKeys())

    return [category_key.GetName() for category_key in file_iterator]

def discover_histograms_by_type(file_name):
    """Discovers the histograms saved in a file with multiple TDirectories.

    Args:
        file_name: the file to be inspected.

    Returns
        histograms: a dictionary with {folder: {type: [histogram_name, ] }]}
    """
    file = ROOT.TFile(file_name)
    file_iterator = ROOT.TIter(file.GetListOfKeys())
    histograms = dict()

    for category_key in file_iterator:
        category = file.Get(category_key.GetName())

        histograms_this_cat = dict()
        for histogram in ROOT.TIter(category.GetListOfKeys()):
            histogram_class = histogram.GetClassName()

            if histogram_class not in histograms_this_cat.keys():
                histograms_this_cat[histogram_class] = [histogram.GetName()]
            else:
                histograms_this_cat[histogram_class] += [histogram.GetName()]

        histograms[category_key.GetName()] = histograms_this_cat

    return histograms
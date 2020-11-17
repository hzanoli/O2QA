from collections import namedtuple

import ROOT


class HistogramInfo(namedtuple('HistogramInfoBase', ['path', 'name', 'root_class'])):
    def __hash__(self):
        return hash('/'.join(self.path) + '/' + self.name)


def is_root_histogram(class_name: str):
    """Returns whether class_name represents a ROOT histogram."""
    if class_name.startswith('TH') or class_name.startswith('TProfile'):
        return True
    return False


def discover_histograms(file_name):
    """Discovers the histograms saved in a file with multiple TDirectories.

    Args:
        file_name: the file to be inspected.

    Returns
        histograms: a list with HistogramInfo for each histogram.
    """
    file = ROOT.TFile(file_name)
    file_iterator = ROOT.TIter(file.GetListOfKeys())
    histograms = list()

    path = []
    it = file_iterator
    loop_list(path, it, histograms, file)

    return histograms


def loop_list(path, it, histograms, directory):
    for key in it:
        if is_root_histogram(key.GetClassName()):
            histogram = HistogramInfo(path, key.GetName(), key.GetClassName())
            histograms.append(histogram)
        else:
            new_path = path + [key.GetName()]
            new_directory = directory.Get(key.GetName())
            iterator_dir = ROOT.TIter(new_directory.GetListOfKeys())
            loop_list(new_path, iterator_dir, histograms, new_directory)

    # for category_key in file_iterator:
    #     category = file.Get(category_key.GetName())
    #
    #     for hist_or_dir in ROOT.TIter(category.GetListOfKeys()):
    #         if is_root_histogram(hist_or_dir.GetClassName()):
    #             histogram = HistogramInfo(category_key.GetName(), None, hist_or_dir.GetName(), hist_or_dir.GetClassName())
    #             histograms.append(histogram)
    #
    #         else:
    #             sub_category = category.Get(hist_or_dir.GetName())
    #
    #             for hist in ROOT.TIter(sub_category.GetListOfKeys()):
    #                 histogram = HistogramInfo(category_key.GetName(), hist_or_dir.GetName(),
    #                                           hist.GetName(), hist.GetClassName())
    #                 histograms.append(histogram)

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

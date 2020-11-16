import pytest

import O2SingleTrackQA.file_utils as file

def test_is_root_histogram():
    root_histogram_names = ['TH1I', 'TH2F', 'TH3D', 'TProfile', 'TProfile2D']

    for type_hist in root_histogram_names:
        assert file.is_root_histogram(type_hist) is True

#def

def test_discover_histograms():
    pass
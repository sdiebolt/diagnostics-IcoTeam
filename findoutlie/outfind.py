""" Module with routines for finding outliers
"""
import numpy as np

from pathlib import Path

from .detectors import iqr_detector
from .spm_funcs import get_spm_globals


def detect_outliers(fname):
    return np.argwhere(iqr_detector(get_spm_globals(fname)))


def find_outliers(data_directory):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = Path(data_directory).glob('**/sub-*.nii.gz')
    outlier_dict = {}
    for fname in image_fnames:
        outliers = detect_outliers(fname)
        outlier_dict[fname] = outliers
    return outlier_dict

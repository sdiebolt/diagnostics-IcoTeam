""" Scan outlier metrics
"""
import numpy as np


def dvars(img):
    """ Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the mean of the (voxel differences squared)).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumes in `img`.
    """
    data = img.get_fdata().reshape(-1, img.shape[-1])
    data_diff_squared = np.diff(data) ** 2
    return np.sqrt(np.mean(data_diff_squared, axis=0))

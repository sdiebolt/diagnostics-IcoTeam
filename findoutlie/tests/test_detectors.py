"""Test script for detector functions.

To run these scripts, use pytest, e.g. 

    pytest findoutlie/tests/

"""

import numpy as np

from pathlib import Path

from ..detectors import iqr_detector

def test_iqr_detector():
    # From: http://www.purplemath.com/modules/boxwhisk3.htm
    example_values = np.array(
        [10.2, 14.1, 14.4, 14.4, 14.4, 14.5, 14.5, 14.6, 14.7, 14.7, 14.7,
         14.9, 15.1, 15.9, 16.4])
    is_outlier = iqr_detector(example_values, 1.5)
    assert np.all(example_values[is_outlier] == [10.2, 15.9, 16.4])
    # Test not-default value for outlier proportion
    is_outlier = iqr_detector(example_values, 0.5)
    assert np.all(example_values[is_outlier] == [10.2, 14.1, 15.1, 15.9, 16.4])

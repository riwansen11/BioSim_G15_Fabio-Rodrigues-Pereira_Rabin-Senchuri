# -*- coding: utf-8 -*-

import random
import pytest
import math
import numpy as np
# from pytest import approx
from src.biosim.geography import Cells, Jungle, Savannah, Desert, \
    Ocean, Mountain

"""
This is the geography pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


def test_check_unknown_parameters():
    """Test method 'check_unknown_parameters()' if it does not
    identifies the given parameter and returns ValueError"""
    with pytest.raises(ValueError):
        Jungle.check_unknown_parameters(params={'f_min': 100})
        Savannah.check_unknown_parameters(params={'f_min': 100})


def test_check_known_parameters():
    """Test method 'check_unknown_parameters()' if it identifies the
    given parameter and does not return ValueError"""
    Jungle.check_unknown_parameters(params={'f_max': 100})
    Savannah.check_unknown_parameters(params={'f_max': 100})


def test_now_negative_parameters():
    """Test method 'check_non_negative_parameters(param_key, params)'
    if it identifies the negative value of a given parameter and returns
    ValueError"""
    param_key, params = 'f_max', {'f_max': 1}
    Jungle.check_non_negative_parameters(param_key, params)
    Savannah.check_non_negative_parameters(param_key, params)



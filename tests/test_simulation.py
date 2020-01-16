# -*- coding: utf-8 -*-

import random
import pytest
import math
import numpy as np
# from pytest import approx
from src.biosim.simulation import BioSim

"""
This is the simulation pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


def test_neighbour_cells():
    """Test if returns the 4ths neighbour_object cells"""
    island_map = "OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (2, 3),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (2, 1),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (1, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (3, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
        }
    ]

    BioSim(island_map, ini_pop, None)



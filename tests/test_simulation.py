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


def test_num_animals():
    """Test if the method 'num_animals()' correctly gets the entire
    population of the island and test if the method
    num_animals_per_species() generates a dictionary with the animal
    species and their island population number"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]},
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]},
        {"loc": (1, 3),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20}]}]

    t = BioSim(island_map, ini_pop, None)
    assert t.num_animals is 7
    assert type(t.num_animals_per_species) is dict
    num_herb = t.num_animals_per_species['Herbivore']
    num_carn = t.num_animals_per_species['Carnivore']
    assert num_herb is 4
    assert num_carn is 3

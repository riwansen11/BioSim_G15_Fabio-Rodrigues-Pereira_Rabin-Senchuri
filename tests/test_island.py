# -*- coding: utf-8 -*-

"""
This is the island pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import textwrap
import pytest
from src.biosim.simulation import BioSim
from src.biosim.island import Island
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from src.biosim.fauna import Herbivore, Carnivore


def test_island_boundary():
    """Raises ValueError if boundary of island is other than "O"""
    island_map = """\
                    OOOSOOO
                    OODSSJO
                    JJJJSSO
                    OSSSJJJ
                    OOOOOOO
    
                 """
    island_map = textwrap.dedent(island_map)
    with pytest.raises(ValueError):
        Island(island_map)


def test_island_length():
    """Raises ValueError if length of island is same on each row"""
    island_map = """\
                        OOOSOOO
                        OODSSJO
                        JJJJSSOO
                        OSSSJJJ
                        OOOOOOOJJJ

                     """
    island_map = textwrap.dedent(island_map)
    with pytest.raises(ValueError):
        Island(island_map)


def test_island_character():
    island_map = """\
                            OOOSOOO
                            OODQSJO
                            JJJJSSS
                            OSPPJJJ
                            OOOOOOO"""

    island_map = textwrap.dedent(island_map)
    with pytest.raises(ValueError):
        Island(island_map)


def test_neighbour_cells():
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

    a = BioSim(island_map, ini_pop, None)
    loc = (2, 2)
    print(a.island.neighbour_cell(loc))
    '''[<src.biosim.geography.Jungle object at 0x10d696a90>, ...,
    <src.biosim.geography.Jungle object at 0x10d696b10>]'''

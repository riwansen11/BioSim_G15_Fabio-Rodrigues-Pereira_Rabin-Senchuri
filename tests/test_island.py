import random
import pytest
import math
import numpy as np
# from pytest import approx
from src.biosim.island import Island
from src.biosim.simulation import BioSim
import textwrap

"""
This is the island pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


def test_island_boundary():

    """
    Raises ValueError if boundary of island is other than "O"
    """

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
    """
       Raises ValueError if length of island is same on each row
       """
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
                            OOOOOOO

                         """
    island_map = textwrap.dedent(island_map)
    with pytest.raises(ValueError):
        Island(island_map)


def test_add_population_in_island():
    pass


def test_geography_cells():
    pass




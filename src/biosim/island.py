# -*- coding: utf-8 -*-
import textwrap
from src.biosim.geography import Geography
from src.biosim.fauna import Fauna

"""
This is the Island model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Island:
    def __init__(self, island_map):
        island_map = textwrap.dedent(island_map).splitlines()
        self.geo = Geography(island_map)
        self.island = self.geo.cells()

        self.population = []

    def set_parameters(self, species, params):
        pass

    def add_population(self, population):
        pass

    def yearly_cycle(self):
        pass



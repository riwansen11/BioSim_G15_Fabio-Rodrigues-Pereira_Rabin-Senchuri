# -*- coding: utf-8 -*-

import textwrap
from random import random
from operator import attrgetter

from src.biosim.animals import Animal
from src.biosim.animalOgen import AnimalObject

"""
This is the landscape model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Map:
    """
    Here there are methods useful to identify and organize the
    geography of any given region.
    """
    example_geogr = """\
                   OOOOOOOOOOOOOOOOOOOOO
                   OOOOOOOOSMMMMJJJJJJJO
                   OSSSSSJJJJMMJJJJJJJOO
                   OSSSSSSSSSMMJJJJJJOOO
                   OSSSSSJJJJJJJJJJJJOOO
                   OSSSSSJJJDDJJJSJJJOOO
                   OSSJJJJJDDDJJJSSSSOOO
                   OOSSSSJJJDDJJJSOOOOOO
                   OSSSJJJJJDDJJJJJJJOOO
                   OSSSSJJJJDDJJJJOOOOOO
                   OOSSSSJJJJJJJJOOOOOOO
                   OOOSSSSJJJJJJJOOOOOOO
                   OOOOOOOOOOOOOOOOOOOOO"""

    def __init__(self, geogr=None):
        """
        :param geogr: Multi-line string specifying a region's geography
        ('O' = Ocean, 'S' = Savannah, 'M' = Mountain, 'J' = Jungle,
        'D' = Desert) divided by cells.
        """
        self.geogr = textwrap.dedent(Map.example_geogr) \
            if geogr is None else textwrap.dedent(geogr)

    def geolist(self):
        """
        Calls .splitlines() to create a list of strings with each
        line of the geogr's string as an element, such that as example:
        ['OOOOOOOOOOOOOOOOOOOOO', 'OOOOOOOOSMMMMJJJJJJJO', ...],
        and then creates a list with a list with splitted strings as
        elements.

        :return: The list with a list with splitted strings, such that as
        example: [['O', 'O', ..., 'O', 'O'], ['O', 'O', ..., 'J',
        'O'], ...].
        """
        return [list(g) for g in self.geogr.splitlines()]

    def cell_coordinate(self):
        """
        Creates the cell's coordinates where i is the row number
        and j is the column number.

        :return: A list with tuple with coordinates (i, j) for each
        cell of the identified geography of a map, such that as example:
        """
        pass

    def coordinates_object(self):
        coord = self.geolist()
        for rownum, row in enumerate(coord):
            for colnum, itemvalue in enumerate(row):
                if coord[rownum][colnum] == 'O':
                    coord[rownum][colnum] = Ocean((rownum, colnum))
                elif coord[rownum][colnum] == 'M':
                    coord[rownum][colnum] = Mountain((rownum, colnum))
                elif coord[rownum][colnum] == 'D':
                    coord[rownum][colnum] = Desert((rownum, colnum))
                elif coord[rownum][colnum] == 'J':
                    coord[rownum][colnum] = Jungle((rownum, colnum))
                else:
                    coord[rownum][colnum] = Savannah((rownum, colnum))
        return coord


class Geography(Map):
    params_examples = {'J': (800.0, None), 'S': (300.0, 0.3)}

    def __init__(self, geogr):
        super().__init__(geogr)

    @staticmethod
    def k_parameters():
        k_parameters = ('w_birth', 'sigma_birth', 'beta', 'eta',
                        'a_half', 'phi_age', 'w_half', 'phi_weight',
                        'mu', 'lambda', 'gamma', 'zeta', 'xi',
                        'omega', 'F', 'DeltaPhiMax')

    def is_habitable(self, loc):
        """
        Check from a cell's localization (i=rownum, j=colnum) if the
        geography is habitable. Only Jungle ('J'), Savannah ('S') and
        Desert ('D') is habitable.

        :param
            loc: tuple
                Cell's localization (i=rownum, j=colnum) of a map.

        :return: a bol with True or False
        """
        return True if self.geolist()[loc[0]][loc[1]] is 'J' or 'D' or \
                       'S' else False


class Ocean(Geography):
    pass


class Mountain(Geography):
    pass


class Desert(Geography):
    pass


class Savannah(Geography):
    pass


class Jungle(Geography):
    pass
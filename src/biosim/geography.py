# -*- coding: utf-8 -*-

import textwrap
import numpy as np
import random as rd

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Geography:
    """
    Here there are methods useful to identify and organize and check
    restrictions when a geography of any region is given.

    Also creates geography parameters objects
    """

    def __init__(self):
        self.cells = []
        self.jungle_params = {'f_max': 800.0, 'alpha': None}
        self.savannah_params = {'f_max': 300.0, 'alpha': 0.3}
        self.desert_params = {'f_max': None, 'alpha': None}
        self.ocean_params = {'f_max': None, 'alpha': None}
        self.mountain_params = {'f_max': None, 'alpha': None}

    @staticmethod
    def has_invalid_character(geogr):
        """
        Searches for invalid character and raise a ValueError if
        necessary.

        :param geogr: Multi-line string
        """
        geogr = textwrap.dedent(geogr)
        geos_detected = ''.join(set(''.join(geogr.splitlines())))
        for letter in geos_detected:
            if letter not in ('O', 'S', 'M', 'J', 'D'):
                raise ValueError('Invalid character {} '
                                 'identified'.format('< ' + letter +
                                                     ' >'))

    @staticmethod
    def has_same_line_lengths(geogr):
        """
        Checks if the lengths of the lines are equal and raise a
        ValueError if necessary.

        :param geogr: Multi-line string
        """
        line_length, geogr = None, textwrap.dedent(geogr)
        for element in geogr.splitlines():
            if line_length in (None, len(element)):
                line_length = len(element)
            else:
                raise ValueError('Different line lengths detected')

    @staticmethod
    def has_invalid_boundary(geogr):
        """
        Searches for invalid non-ocean boundary character  and raise a
        ValueError if necessary.

        :param geogr: Multi-line string
        """
        pass

    def get_cells(self, geogr):
        """
        Transforms a multi-line string in numpy's array.

        :param geogr: Multi-line string
        """
        geogr = textwrap.dedent(geogr)
        self.has_invalid_character(geogr)
        self.has_same_line_lengths(geogr)
        self.has_invalid_boundary(geogr)

        for row in geogr.splitlines():
            self.cells.append(list(row.strip()))
        """self.cells = np.array([list(line.strip()) for line in
                               geogr.splitlines()])"""

    def is_habitable(self, loc):
        """
        Checks if the cell is habitable.

        :param loc: tuple
        :return: True if habitable or False if not habitable
        """
        return True if self.cells[loc[0]][loc[1]] in ('J', 'S', 'D') \
            else False

    def find_landscape_param(self, landscape):
        """
        Finds any landscape default parameter.

        :param landscape: string
        """
        if landscape in ('J', 'Jungle', 'jungle', 'j'):
            return self.jungle_params

        elif landscape in ('S', 'Savannah', 'savannah', 's'):
            return self.savannah_params

        elif landscape in ('D', 'Desert', 'desert', 'd'):
            return self.desert_params

        elif landscape in ('O', 'Ocean', 'ocean', 'o'):
            return self.savannah_params

        elif landscape in ('M', 'Mountain', 'mountain', 'm'):
            return self.desert_params

        else:
            raise ValueError('Landscape {} not found'.format(landscape))

    def get_parameters(self, landscape=None, params=None):
        """
        Updates any landscape parameter.

        :param landscape: string
        :param params: dict
        """
        if not isinstance(params, dict):
            raise TypeError("'param_dict' must be type 'dict'")
        else:
            for parameter in params.keys():
                if 'f_max' is parameter and params['f_max'] <= 0:
                    raise ValueError(
                        "parameter 'f_max' must be non-negative")
                elif parameter not in \
                        self.find_landscape_param(landscape).keys():
                    raise ValueError(
                        "unknown parameter: '{}'".format(parameter))
            self.find_landscape_param(landscape).update(params)

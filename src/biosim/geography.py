# -*- coding: utf-8 -*-
from src.biosim.fauna import Population

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Geography:

    geo_types = {'O': 'Ocean', 'S': 'Savannah', 'M': 'Mountain',
                 'J': 'Jungle', 'D': 'Desert'}

    parameters = {}

    @classmethod
    def set_parameters(cls, landscape=None, params=None):
        """
        Updates any landscape parameter.

        :param landscape: string
        :param params: dict
        """
        if not isinstance(params, dict):
            raise TypeError("'param_dict' must be type 'dict'")

        else:
            geo = self.find_landscape_type(landscape)
            for parameter in params.keys():
                if 'f_max' is parameter and params['f_max'] <= 0:
                    raise ValueError(
                        "parameter 'f_max' must be non-negative")
                elif parameter not in geo.parameters.keys():
                    raise ValueError(
                        "unknown parameter: '{}'".format(parameter))
            geo.parameters.update(params)

    def __init__(self, geographies):
        self.geos = geographies  # list of cells received

        self.pop = Population(self.geos)  # send
        self.population = self.pop.create_cells()

    def create_cells(self):
        loc = [(i, j) for i in range(len(self.geos))
               for j in range(len(self.geos[0]))]
        geo = [geo for i in range(len(self.geos))
               for geo in self.geos[i]]
        return dict(zip(loc, geo))

    def find_landscape_type(self, landscape):
        """
        Finds any landscape default parameter.

        :param landscape: string
        """
        if landscape in self.geo_types.keys():
            return self.geo_types[landscape]
        else:
            raise ValueError('Geography {} not found'.format(landscape))


class Jungle(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': 800.0, 'alpha': None}


class Savannah(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': 300.0, 'alpha': 0.3}


class Desert(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}


class Ocean(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}


class Mountain(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}

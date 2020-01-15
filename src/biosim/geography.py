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
    def check_unknown_parameter(cls, params):
        for parameter in cls.parameters.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "'{}'".format(parameter))

    @classmethod
    def check_non_negative_f_max_parameter(cls, params):
        for parameter in cls.parameters.keys():
            if 'f_max' is parameter and cls.parameters['f_max'] <= 0:
                raise ValueError("The parameter 'f_max' must be "
                                 "non-negative")

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameter(params)
        cls.check_non_negative_f_max_parameter(params)
        cls.parameters.update(params)

    def __init__(self, geographies):
        self.geos = geographies

        self.pop = Population(self.geos)
        self.population = self.pop.create_cells()

    def create_cells(self):
        loc = [(i, j) for i in range(len(self.geos))
               for j in range(len(self.geos[0]))]
        geo = [geo for i in range(len(self.geos))
               for geo in self.geos[i]]
        return dict(zip(loc, geo))


class Jungle(Geography):
    def __init__(self, geographies):
        super().__init__(geographies)
        self.parameters = {'f_max': 800.0, 'alpha': None}


class Savannah(Geography):
    def __init__(self, geographies):
        super().__init__(geographies)
        self.parameters = {'f_max': 300.0, 'alpha': 0.3}


class Desert(Geography):
    def __init__(self, geographies):
        super().__init__(geographies)
        self.parameters = {'f_max': None, 'alpha': None}


class Ocean(Geography):
    def __init__(self, geographies):
        super().__init__(geographies)
        self.parameters = {'f_max': None, 'alpha': None}


class Mountain(Geography):
    def __init__(self, geographies):
        super().__init__(geographies)
        self.parameters = {'f_max': None, 'alpha': None}

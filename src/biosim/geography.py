# -*- coding: utf-8 -*-
from src.biosim.fauna import Herbivore, Carnivore

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Cells:
    parameters = {}

    @classmethod
    def check_unknown_parameter(cls, params):
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "'{}'".format(parameter))

    @classmethod
    def check_non_negative_f_max_parameter(cls, params):
        for parameter in params.keys():
            if parameter is 'f_max' and parameter['f_max'] <= 0:
                raise ValueError("The parameter 'f_max' must be "
                                 "non-negative")

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameter(params)
        cls.check_non_negative_f_max_parameter(params)
        cls.parameters.update(params)

    def __init__(self):
        self.pop_per_species = {Herbivore: [], Carnivore: []}
        self.new_pop_per_species = {Herbivore: [], Carnivore: []}

    def add_pop(self, individuals):
        for animal in individuals:  # [ Carnivore(age, weight), ...]
            self.pop_per_species[type(animal)].append(animal)


class Jungle(Cells):
    parameters = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder = self.parameters['f_max']  # ****check


class Savannah(Cells):
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder += self.parameters['alpha'] * (
                self.parameters['f_max'] - self.fodder)  # ****check


class Desert(Cells):
    def __init__(self):
        super().__init__()


class Ocean(Cells):
    def __init__(self):
        super().__init__()


class Mountain(Cells):
    def __init__(self):
        super().__init__()

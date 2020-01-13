# -*- coding: utf-8 -*-

import numpy as np
import random
from src.biosim.geography import Geography

"""
This is the fauna model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Fauna(Geography):
    """Creates the fauna object and its parameters"""

    def __init__(self):
        super().__init__()
        self.fauna = []
        self.herbivore_params = {'w_birth': 8.0,
                                 'sigma_birth': 1.5,
                                 'beta': 0.9,
                                 'eta': 0.05,
                                 'a_half': 40.,
                                 'phi_age': 0.2,
                                 'w_half': 10.,
                                 'phi_weight': 0.1,
                                 'mu': 0.25,
                                 'lambda': 1,
                                 'gamma': 0.2,
                                 'zeta': 3.5,
                                 'xi': 1.2,
                                 'omega': 0.4,
                                 'F': 10.0,
                                 'DeltaPhiMax': None}

        self.carnivore_params = {'w_birth': 8.0,
                                 'sigma_birth': 1.5,
                                 'beta': 0.9,
                                 'eta': 0.05,
                                 'a_half': 40.,
                                 'phi_age': 0.2,
                                 'w_half': 10.,
                                 'phi_weight': 0.1,
                                 'mu': 0.25,
                                 'lambda': 1,
                                 'gamma': 0.2,
                                 'zeta': 3.5,
                                 'xi': 1.2,
                                 'omega': 0.4,
                                 'F': 10.0,
                                 'DeltaPhiMax': 10.0}

    def find_specie_param(self, species):
        """
        Finds any specie default parameter.

        :param species: string
        """
        if species in ('H', 'h', 'Herbivore', 'herbivore'):
            return self.herbivore_params

        elif species in ('C', 'c', 'Carnivore', 'carnivore'):
            return self.carnivore_params

        else:
            raise ValueError('Specie {} not found'.format(species))

    def get_parameters(self, species=None, params=None):
        """
        Update any specie parameter.

        :param species: string
        :param params: dict
        """
        if not isinstance(params, dict):
            raise TypeError("params must be type 'dict'")
        else:
            for param in params.keys():
                if param not in self.find_specie_param(species).keys():
                    raise ValueError(
                        "unknown parameter: '{}'".format(param))
            self.find_specie_param(species).update(params)

    def get_population(self, population):
        """

        :param population: List of dictionaries specifying population:
        [{ "loc": (10, 10),
           "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
           "loc": (10, 10),
           "pop": [{"species": "Carnivore", "age": 10, "weight": 05}]}]
        """
        pass
        """
        for i in population:
            loc, pop = i['Loc'], i['pop']
            for pop_data in pop:
                if pop_data['species'] is 'Herbivore':
                    Herbivore.population(loc, pop_data)
                else:
                    Carnivore.population(loc, pop_data)"""

# -*- coding: utf-8 -*-
import numpy as np

"""
This is the fauna model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Population:
    parameters = {}

    @classmethod
    def check_unknown_parameter(cls, params):
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "'{}'".format(parameter))

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameter(params)
        cls.parameters.update(params)

    @classmethod
    def _weight_at_birth(cls, p):
        return np.random.normal(p['w_birth'], p['sigma_birth'])

    def __init__(self, age=0, weight=None):
        if age and (weight is None):
            raise ValueError("cannot set 'age' without passing 'weight'")

        if not isinstance(age, int):
            raise TypeError("'age' must be type: 'int'")

        if weight is not None:
            if not isinstance(weight, (int, float)):
                raise TypeError(
                    "'weight' must be type: 'int' or 'float'")

        if weight is not None:
            if (not 0 < weight) or (not 0 < age):
                raise ValueError("'weight' and 'age' must be a "
                                 "non-negative 'int' or 'float'")

        self.age = age
        self.weight = self._weight_at_birth(self.parameters) \
            if self.age is 0 else weight

        '''self.fitness = self._compute_fitness(self.age, self.weight,
                                             self.parameters)'''


class Herbivore(Population):
    parameters = {'w_birth': 8.0,
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

    def __init__(self, age=0, weight=None):
        super().__init__()


class Carnivore(Population):
    parameters = {'w_birth': 8.0,
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

    def __init__(self, age=0, weight=None):
        super().__init__()

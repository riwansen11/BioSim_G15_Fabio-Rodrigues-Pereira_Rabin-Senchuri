# -*- coding: utf-8 -*-
import random

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
                                 "*{}*".format(parameter))

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameter(params)
        cls.parameters.update(params)

    def __init__(self, age=0, weight=None):
        self.age = age
        self.weight = weight

    def ages(self):
        """
        Returns
        -------
            int
                updated age after each year
        """
        self.age += 1

    def increase_weight(self, feed):
        self.w = self.w + self.default_params["beta"] * feed

    def weight_decrease(self):
        """
        Returns
        -------
            float
                calculate weight the amount of weight decrease
        """
        self.w = self.w - (self.default_params["eta"] * self.w)
        self.update_fitness()

    @staticmethod
    def q(sgn, x, xhalf, phi):
        """

        Parameters
        ----------
        sgn
        x
        xhalf
        phi

        Returns
        -------
            float
                method to calculate fitness
        """
        return 1. / (1. + np.exp(sgn * phi * (x - xhalf)))

    def fitness(self):
        """
        Returns
        -------
            float
                Calculated fitness of an animal
        """
        if self.w == 0:
            return 0
        else:
            return (self.q(+1, self.age, self.default_params["a_half"], self.default_params["phi_age"])
                    * self.q(-1, self.w, self.default["w_half"], self.default_params["phi_weight"]))

    def birth(self, N):
        """
        Parameters
        ----------
            N: int
             number of animals present

        Returns
        -------
            int
                number of newborns
        """

        K = self.zeta * (self.default_params["w_birth"] + self.default_params["sigma_birth"])
        a = min(1, self.default_params["gamma"] * self.fitness * (N - 1))
        return random.random() < a and self.w > K

    def update_weight_after_birth(self, weight):
        self.w = self.default_params["xi"] * weight
        self.update_fitness()

    def update_fitness(self):
        """
        Re-calculates the fitness based on updated values of age and
        weight.

        """
        self.fitness = self.fitness(self.age, self.w)

    def death(self):
        """
        Returns
        -------
            True when animal died
            False when animal not died
        """
        if self.fitness == 0:
            return True
        elif random.random() < self.default_params["omega"] * (1 - self.fitness):
            return True
        else:
            return False

    def h_eating_rule(self, f):
        """
            Eating rule for Herbivore Animals

            Compare the available food in the cell and amount of fodder
            to be eaten

            Returns the amount eaten by a Herbivore
        """
        if f <= self.F:
            eaten = f
        else:
            eaten = self.F

        self.w += self.beta * eaten
        return eaten

    def coordinations(self):
        animals = []
        for i in range(50):
            for j in range(50):
                animals.append((random.randint(1, 22),
                                random.randint(1, 21)))
        return animals

    def migration_chances(self):
        migrate_chances = random.random() < self.default_params["mu"] * self.fitness()
        return migrate_chances


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

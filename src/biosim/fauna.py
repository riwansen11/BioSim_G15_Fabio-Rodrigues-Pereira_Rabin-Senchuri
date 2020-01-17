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

    @staticmethod
    def fitness_formula(sgn, x, xhalf, phi):
        return 1.0 / (1 + np.exp(sgn * phi * (x - xhalf)))

    @classmethod
    def check_unknown_parameters(cls, params):
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameters(params)
        cls.parameters.update(params)

    def __init__(self, age=0, weight=None):

        self.age = age
        self.weight = random.gauss(self.parameters['w_birth'],
                                   self.parameters['sigma_birth']) \
            if weight is None else weight

        self.fitness = self.calculate_fitness()

    def get_old(self):
        self.age += 1

    def gain_weight(self, feed):
        self.weight = self.weight + self.parameters["beta"] * feed

    def lose_weight(self):
        self.weight = self.weight - (self.parameters["eta"] *
                                     self.weight)
        self.update_fitness()

    def calculate_fitness(self):
        return 0 if self.weight is 0 else \
            (self.fitness_formula(+1, self.age,
                                  self.parameters['a_half'],
                                  self.parameters['phi_age']) *
             self.fitness_formula(-1, self.weight,
                                  self.parameters['w_half'],
                                  self.parameters['phi_weight']))

    def add_newborns(self, number_specie_objects):
        k = self.parameters['zeta'] * (self.parameters['w_birth'] +
                                       self.parameters['sigma_birth'])

        a = min(1, self.parameters['gamma'] * self.fitness *
                (number_specie_objects - 1))

        return random.random() < a and self.weight > k

    def update_weight_after_birth(self, weight):
        self.weight = self.parameters['xi'] * weight
        self.update_fitness()

    def update_fitness(self):
        self.fitness = self.calculate_fitness()

    def die(self):
        if self.fitness is 0:
            return True
        elif random.random() < self.parameters['omega'] * \
                (1 - self.fitness):
            return True
        else:
            return False

    def migration_chances(self):
        return random.random() < self.parameters['mu'] * self.fitness()


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
        super().__init__(age, weight)

    def herb_eating(self, f):
        self.weight += self.parameters['beta'] * f
        self.update_fitness()


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
        super().__init__(age, weight)

    def carn_eating_rule(self, herb_list):
        feed = 0
        c_fitness = self.calculate_fitness()
        for herb in herb_list:
            h_fitness = herb.calculate_fitness()
            if h_fitness >= c_fitness:
                prob = 0
            elif 0 < (c_fitness - h_fitness) < self.parameters['DeltaPhiMax']:
                prob = (c_fitness - h_fitness) / self.parameters['DeltaPhiMax']
            else:
                prob = 1
            # check if animal gets eaten
            if random.random() < prob:
                feed += herb.weight
                herb_list.remove(herb)

                if feed >= self.parameters['F']:
                    break
        self.gain_weight(feed)
        self.update_fitness()



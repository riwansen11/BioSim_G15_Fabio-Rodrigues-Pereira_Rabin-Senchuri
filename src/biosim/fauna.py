# -*- coding: utf-8 -*-

"""
This is the Fauna model which functions with the BioSim package written
for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import random as rd
import math as math


class Population:
    parameters = {}

    @staticmethod
    def fit_formula(x, x_half, phi_x):
        """This method returns the fitness formula used to calculate
        the physical condition (fitness) of an animal (pop_object).

        * Parameters:   x:          int or float:   'age'
                                                    'weight'
                        x_half:     int or float:   'age_half'
                                                    'weight_half'
                        phi_x:   int or float:      'phi_age'
                                                    'phi_weight'

        * Formula: 1 / {1 + exp[phi_x('x' - 'x_1/2')]}.

        * Where used: calculate_fitness().

        * returns: fit_formula: int or float.
        """
        return 1.0 / (1 + math.exp(phi_x * (x - x_half)))

    @classmethod
    def check__phi_borders(cls, _phi):  # tested
        """Check if the _phi calculated by the method
        'calculate_fitness()' is inside of its required result
        borders '0 <= _phi <= 1'."""
        if not 0 <= _phi <= 1:
            raise ValueError("The parameter '_phi' calculated "
                             "is not in its borders 0 <= _phi <= 1")

    @classmethod  # tested
    def check_unknown_parameters(cls, params):
        """This method checks unknwn parameters."""
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod  # tested
    def set_parameters(cls, params):
        """This method sets the parameter for the animals."""
        cls.check_unknown_parameters(params)
        cls.parameters.update(params)

    def __init__(self, age=0, weight=None):
        self.age = age
        self.weight = rd.gauss(self.parameters['w_birth'],
                               self.parameters['sigma_birth']) \
            if weight is None else weight

        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        """This method calculates and returns the overall physical
        condition (fitness) of an animal which is based on age and
        weight using the formula:

        _phi = if omega <= 0: 0
               else: fit_formula('age', 'age_1/2', 'phi_age') X
                     fit_formula(-'weight', 'weight_1/2', 'phi_weight')

        * Method(s) required: fit_formula(x, x_half, phi_x).

        * returns: _phi: int or float.
        """
        _phi = 0 if self.weight <= 0 \
            else (self.fit_formula(self.age,
                                   self.parameters['a_half'],
                                   self.parameters['phi_age']) *
                  self.fit_formula(-1 * self.weight,
                                   self.parameters['w_half'],
                                   self.parameters['phi_weight']))
        self.check__phi_borders(_phi)
        return _phi

    def get_old(self):  # tested
        """This method increases the age of the animal, in yearly
        basis, by 1 year."""
        self.age += 1

    def gain_weight(self, ate):
        """This method increases the weight of the animal, in yearly
        basis, by the amount eaten times 'beta'."""
        self.weight += self.parameters["beta"] * ate

    def lose_weight(self):
        """This method decreases the weight of the animal, in yearly
        basis, according to the weight_loss_rate.

        * Formulas: weight_loss_rate:       'eta' * 'weight'
                    yearly_weight_loss:     'weight' - 'weight_loss_rate'

        * Notes: After the weight is decreased, the fitness of the
        animal is updated by the method 'update_fitness()'.
        """
        weight_loss_rate = self.parameters["eta"] * self.weight
        yearly_weight_loss = self.weight - weight_loss_rate
        self.weight = yearly_weight_loss
        self.update_fitness()

    def update_fitness(self):
        """This method updates the calculation of parameter fitness of
        the animal."""
        self.fitness = self.calculate_fitness()

    def birth(self, number_specie_objects):
        """
        This method calculates the probability of giving birth
        according to the following conditions:

        1. if the number of animals of a species is 1, then the
        probability is 0;

        2. The probability is also 0 if the weight of the animal is
        less than 'zeta' * ('w_birth' + 'sigma_birth');

        3. Else, the probability is the minimum between 1 or 'gamma' *
        the animal fitness * (number of animals of the specie - 1);

        * Note: The rd.random() is used to get a random number and
        check if is less than the probability of birth, then there is
        a offspring or not.

        :param number_specie_objects: int with the number of animals
                                      of a specie.

        :return: True if the animal gives birth else False.
        """

        k = self.parameters['zeta'] * (self.parameters['w_birth'] +
                                       self.parameters['sigma_birth'])

        if number_specie_objects is 1:
            p = 0
        elif self.weight < k:
            p = 0
        else:
            p = min(1, self.parameters['gamma'] * self.fitness *
                    (number_specie_objects - 1))

        return rd.random() < p

    def update_weight_after_birth(self, baby_weight):
        """This method, when called, updates the with of the animal
        after gives birth, according to the formula: 'xi' * the baby
        weight. Then it updates the fitness."""
        self.weight = self.parameters['xi'] * baby_weight
        self.update_fitness()

    def migration_chances(self):
        """This method calculates the migration probability according to
        the animal fitness times the parameter 'mu'.

        * Note: The rd.random() is used to get a random number and
        check if is less than the probability of migration, then a
        animal migrates or not.

        :returns    True if the animal migrates else False.
        """
        prob_move = self.parameters['mu'] * self.fitness
        rand_num = rd.random()
        return rand_num < prob_move

    def die(self):
        """An animal dies:
         1. with certainty if its fitness is 0;
         2. with probability if 'omega' * (1 - its fitness).

         :return: True if the animal dies else False.
         """
        if self.fitness is 0:
            return True
        elif rd.random() < self.parameters['omega'] * \
                (1 - self.fitness):
            return True
        else:
            return False


class Herbivore(Population):
    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                  'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                  'w_half': 10., 'phi_weight': 0.1, 'mu': 0.25,
                  'lambda': 1, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                  'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)


class Carnivore(Population):
    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                  'eta': 0.125, 'a_half': 60.0, 'phi_age': 0.4,
                  'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
                  'lambda': 1, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                  'omega': 0.9, 'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def is_herb_killed(self, h_fitness):
        """This method decides if a Carnivore will kill a prey
        (Herbivore) according to the following conditions:

        1. If phi_carn <= phi_herb:     p = 0
        2. If 0 < 'phi_carn' - 'phi_herb' < 'DeltaPhiMax':
                                        p = ('phi_carn' - 'phi_herb')
                                            /'DeltaPhiMax'
        3. otherwise:                   p =   1

        :where:     'phi_herb':    h_fitness:   The herbivore fitness
                    'phi_carn':    c_fitness:   The carnivore fitness
                    'DeltaPhiMax:  d_phi_max:

        *Note:      The rd.random() is used to get a random number and
                    check if is less than p, then a herbivore is
                    killed or the herbivore escaped.

        :returns    True if herbivore is killer else False.
        """
        d_phi_max = self.parameters['DeltaPhiMax']
        c_fitness = self.fitness

        if c_fitness <= h_fitness:
            p = 0
        elif 0 < c_fitness - h_fitness < d_phi_max:
            p = (c_fitness - h_fitness) / d_phi_max
        else:
            p = 1
        rand_num = rd.random()
        return rand_num < p

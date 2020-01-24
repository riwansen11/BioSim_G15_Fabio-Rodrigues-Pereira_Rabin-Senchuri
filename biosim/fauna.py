# -*- coding: utf-8 -*-

"""
This is the Fauna model which functions with the BioSim package written
for the INF200 project January 2019..
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import numba
import numpy as np


class Population:
    parameters = {}

    def __init__(self, age=0, weight=None):
        """Constructor for the animals's population."""
        self.age = age
        self.weight = np.random.normal(self.parameters['w_birth'],
                                       self.parameters['sigma_birth']) \
            if self.age is 0 else weight

        self.fitness = self.calculate_fitness(self.age, self.weight,
                                              self.parameters)

    @staticmethod
    @numba.jit
    def fit_formula(sign, x, x_half, phi_x):
        """This method returns the fitness formula used to calculate
        the physical condition (fitness) of an animal (pop_object).

        Formula and conditions:
        ----------
        1.0 / (1 + \\e^{\\pm * \\phi * (x - x_{1/2} )})

        Parameters:
        ----------
            sign: int or float
                The sign with identifies age (+) or weight (-);

            x:  int or float
                This is age or weight;

            x_half: int or float
               This is the parameter 'age_half' or 'weight_half';

            phi_x: int or float
                This is the parameter 'phi_age' or 'phi_weight'.

        Returns:
        ----------
            The fitness formula calculated in float type.
        """
        return 1.0 / (1 + np.exp(sign * phi_x * (x - x_half)))

    @classmethod
    def calculate_fitness(cls, age, weight, parameters):
        """This method calculates and returns the overall physical
        condition (fitness) of an animal which is based on age and
        weight using the formula:

        Formula and conditions:
        ----------
            phi = if 'omega' <= 0: 0
                  else: fit_formula('age', 'age_1/2', 'phi_age') X
                     fit_formula(-'weight', 'weight_1/2', 'phi_weight')

        Parameters:
        ----------
            age: int or float

            weight:  int or float

            parameters: str

        Returns:
        ----------
            phi: int or float
        """
        if weight is 0:
            phi = 0
        else:
            phi = cls.fit_formula(1, age,
                                  parameters['a_half'],
                                  parameters['phi_age']) \
                  * cls.fit_formula(-1, weight,
                                    parameters['w_half'],
                                    parameters['phi_weight'])
        cls.check__phi_borders(phi)
        return phi

    @classmethod
    def check__phi_borders(cls, phi):
        """Check if the _phi calculated by the method
        'calculate_fitness()' is inside of its required result
        borders '0 <= phi <= 1' and raises a ValueError if necessary.

        Parameters:
        ----------
            phi: int or float
        """
        if not 0 <= phi <= 1:
            raise ValueError("The parameter 'phi' calculated "
                             "is not in its borders 0 <= phi <= 1")

    @classmethod
    def check_unknown_parameters(cls, params):
        """This method checks unknown parameters and raises a ValueError
        if necessary.

        Parameters:
        ----------
            params: dict
        """
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameters for the animals.

        Parameters:
        ----------
            params: dict
        """
        cls.check_unknown_parameters(params)
        cls.parameters.update(params)

    def gain_weight(self, amount_eaten):
        """This method increases the weight of the animal, in yearly
        basis, by the amount eaten times 'beta'.

        Parameters:
        ----------
            amount_eaten: int or float
        """
        self.weight += self.parameters['beta'] * amount_eaten
        self.update_fitness()

    def update_weight_after_birth(self, newborn_weight):
        """This method, when called, updates the with of the animal
        after gives birth, according to the formula: 'xi' * the baby
        weight. Then it updates the fitness.

        Parameters:
        ----------
            newborn_weight: int or float
        """
        self.weight -= self.parameters['xi'] * newborn_weight
        self.update_fitness()

    def update_fitness(self):
        """This method updates the calculation of the parameter
        fitness of the animal."""
        self.fitness = self.calculate_fitness(self.age,
                                              self.weight,
                                              self.parameters)

    def birth(self, number_specie_objects):
        """This method calculates the probability of giving birth
        according to the following conditions:

        Formula and conditions:
        ----------
            -> If the number of animals of a species is 1, then the
               probability is 0;
            -> The probability is also 0 if the weight of the animal is
               less than 'zeta' * ('w_birth' + 'sigma_birth');
            -> Else, the probability is the minimum between 1 or
               'gamma' * the animal fitness * (number of animals of
               the specie - 1);
            -> The rd.random() is used to get a random number and
               check if is less than the probability of birth, then,
               if True, there is a offspring, else there is not.

        Parameters:
        ----------
            number_specie_objects: int or float

        Returns:
        ----------
            True if the animal gives birth else False.
        """
        k = self.parameters['zeta'] * (self.parameters['w_birth'] +
                                       self.parameters['sigma_birth'])

        if number_specie_objects is 1:
            p = 0
        else:
            p = min(1, self.parameters['gamma'] * self.fitness *
                    (number_specie_objects - 1))

        return np.random.random() < p and self.weight > k

    def will_kill(self, prey_fitness):
        """This method decides if a Carnivore will kill a prey
        (Herbivore) according to the following conditions:

        Formula and conditions:
        ----------
            -> If fitness of the carnivore <= fitness of the herbivore,
               then p = 0;
            -> If 0 < ('fitness of the carnivore' -  'fitness of the
               herbivore') < 'DeltaPhiMax', then p = ('fitness of the
               carnivore' - 'fitness of the herbivore') / 'DeltaPhiMax';
            -> Otherwise: p =   1.
            -> The rd.random() is used to get a random number and
               check if is less than p, then a herbivore is killed or
               the herbivore escapes.

        Parameters:
        ----------
            prey_fitness: int or float

        Returns:
        ----------
            True if herbivore is killer else False.
        """
        hunter_fitness = self.fitness
        hunter_prey_diff_fitness = hunter_fitness - prey_fitness
        d_phi_max = self.parameters['DeltaPhiMax']

        if hunter_fitness <= prey_fitness:
            p = 0
        elif 0 < hunter_prey_diff_fitness < d_phi_max:
            p = hunter_prey_diff_fitness / d_phi_max
        else:
            p = 1

        return np.random.random() < p

    def will_migrate(self):
        """This method calculates the probability of moving to a
        habitable neighbour cell. This takes in consideration the
        parameter 'mu' times the animal fitness. Both species have the
        chance of migrating, once a year, to north, south, west and east.

        Formula and conditions:
        ----------
            -> If np.random.random() number is less than the migrating
               probability, then an animal migrates, else does not.

        Returns
        ----------
            True if an animal migrates else False.
        """
        return np.random.random() < self.parameters['mu'] * self.fitness

    def get_old(self):
        """This method increases the age of the animal, in yearly
        basis, by 1 year."""
        self.age += 1

    def lose_weight(self):
        """This method decreases the weight of the animal, in yearly
        basis, according to the weight_loss_rate.

        Formula and conditions:
        ----------
            -> weight_loss_rate: 'eta' * 'weight';
            -> yearly_weight_loss: 'weight' - 'weight_loss_rate';
            -> After the weight is decreased, the fitness of the
               animal is updated by the method 'update_fitness()'.
        """
        self.weight -= self.parameters['eta'] * self.weight
        self.update_fitness()

    def will_die(self):
        """An animal dies:

        Formula and conditions:
        ----------
            -> If its fitness is 0, or
            -> With probability if 'omega' * (1 - animal_fitness).
            -> If np.random.random() number is less than the die
               probability, then an animal dies, else does not.

        Returns
        ----------
            True if the animal dies else False.
         """
        return True if self.fitness is 0 else \
            np.random.random() < self.parameters['omega'] * (
                    1 - self.fitness)


class Herbivore(Population):
    """The herbivores find fodder in savannah and jungle, although
    they can reside in desert also."""
    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                  'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                  'w_half': 10., 'phi_weight': 0.1, 'mu': 0.25,
                  'lambda': 1, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                  'omega': 0.4, 'F': 10.0}

    def __init__(self, age=0, weight=None):
        """Constructor for Herbivore class."""
        super().__init__(age, weight)


class Carnivore(Population):
    """The carnivores prey on herbivores in savannah, jungle and
    desert."""
    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                  'eta': 0.125, 'a_half': 60.0, 'phi_age': 0.4,
                  'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
                  'lambda': 1, 'gamma': 0.8, 'zeta': 3.5, 'xi': 1.1,
                  'omega': 0.9, 'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, age=0, weight=None):
        """Constructor for Carnivore class."""
        super().__init__(age, weight)

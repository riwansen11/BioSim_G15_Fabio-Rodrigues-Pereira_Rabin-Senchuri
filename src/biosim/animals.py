import numpy as np
import random


class Animal:
    """Sets different parameters for animals

       Parameters
       ----------
        age: int
            Age of each animal
        weight: int
            Weight of an animal

    """

    def __init__(self, age=0, weight=None):
        """Create animal with age 0 and weight 0."""

        self.age = age
        if weight is None:
            self.w = random.gauss(self.w_birth, self.sigma_birth)
        else:
            self.w = weight
        self.fitness = self.fitness()

    @classmethod
    def set_params(cls, params=None):
        """
        Sets class parameters

        Parameters
        ----------
            params: dict
                parameter dictionary {'param':value}

        Returns
        -------
            None
                None
        """
        if not isinstance(params, dict):
            raise TypeError("params must be type 'dict'")
        for param in params.keys():
            if param in cls.default_params:
                raise ValueError(
                    "unknown parameter: '{}'".format(param))

        cls.default_params.update(params)

    def ages(self):
        """
        Returns
        -------
            int
                updated age after each year
        """
        self.age += 1

    def increase_weight(self, feed):
        self.w = self.w + self.beta * feed

    def weight_decrease(self):
        """
        Returns
        -------
            float
                calculate weight the amount of weight decrease
        """
        self.w = self.w - (self.eta * self.w)
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
            return (self.q(+1, self.age, self.a_half, self.phi_age)
                    * self.q(-1, self.w, self.w_half, self.phi_weight))

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

        K = self.zeta * (self.w_birth + self.sigma_birth)
        a = min(1, self.gamma * self.fitness * (N - 1))
        if random.random() < a and self.w > K:
            newborn = self.__class__()
            self.w -= (self.xi * newborn.w)  # mother loses weight xi
            self.update_fitness()
            return newborn
        else:
            return None

    def update_fitness(self):
        """
        Re-calculates the fitness based on updated values of age and
        weight.

        """
        self.fitness = self.fitness

    def death(self):
        """
        Returns
        -------
            True when animal died
            False when animal not died
        """
        if self.fitness == 0:
            return True
        elif random.random() < self.omega * (1 - self.fitness):
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


class Herbivore(Animal):
    """
    Sets default parameters for Herbivore animals

    Takes Animal as super-class to calculate different parameters
    """
    default_params = {'w_birth': 8.0,
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
                      'F': 10.0}

    w_birth = default_params['w_birth']
    sigma_birth = default_params['sigma_birth']
    beta = default_params['beta']
    eta = default_params['eta']
    a_half = default_params['a_half']
    phi_age = default_params['phi_age']
    w_half = default_params['w_half']
    phi_weight = default_params['phi_weight']
    mu = default_params['mu']
    gamma = default_params['gamma']
    zeta = default_params['zeta']
    xi = default_params['xi']
    omega = default_params['omega']
    F = default_params['F']

    def __init__(self, age=0, weight=None):
        """
        Constructor for super class

        Parameters
        ----------
            age: int
                age of an animal
            weight: float
                weight of an animal
        """
        super().__init__(age, weight)

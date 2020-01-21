# -*- coding: utf-8 -*-

"""
This is the Geography model which functions with the BioSim package
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import numpy as np
from biosim.fauna import Herbivore, Carnivore


class Cells:
    parameters = {}

    @staticmethod
    def cumsum(migrating_specie, neighbours):
        """This method generates a list with the probabilities of
        migrating of a given animal according to its neighbours.

        Formula and conditions:
        ----------
            Prob = propensity / sum([all_propensities])

        Parameters:
        ----------
            migrating_specie: str
                String with 'Herbivore' or 'Carnivore';

            neighbour: list
                List with, i.e., [Jungle, Savannah, ...].

        Returns:
        ----------
            List with probabilities.
        """
        propensities = [neighbour.propensities(migrating_specie,
                                               neighbour)
                        for neighbour in neighbours]

        prob = [propensity / sum(propensities)
                for propensity in propensities]

        return np.cumsum(prob)

    @staticmethod
    def propensities(migrating_specie, neighbour):
        """This method calculates the propensity (phi_i_j) of a given
        animal to move to a 'J', 'S' or 'D' landscapes.

        Formula and conditions:
        ----------
            phi_i_j =   0 if mountain or ocean, or
                        exp('lambda' * 'e_k') if 'J', 'S' or 'D'

        for:
            -> 'lambda' = 0: all possible destination cells will be
                chosen with equal probability;
            -> 'lambda' > 0: The animal prefers cells with the greater
                abundance of food;
            -> 'lambda' < 0: The animal turn away from food.

        Parameters:
        ----------
            migrating_specie: str
                String with 'Herbivore' or 'Carnivore';

            neighbour: <class 'type'>
                The landscape neighbour object.

        Returns:
        ----------
            Int with the propensity of a given specie in a landscape.
        """
        e_k = neighbour.relative_abundance(migrating_specie, neighbour)
        if migrating_specie is 'Herbivore':
            return np.exp(Herbivore.parameters['lambda'] * e_k)
        else:
            return np.exp(Carnivore.parameters['lambda'] * e_k)

    @staticmethod
    def relative_abundance(migrating_specie, neighbour):
        """This is the relative abundance of fodder (e_k) that is used to
        calculated the propensity in the method 'propensity()'.

        Formula and conditions:
        ----------

        e_k = f_k / [(n_k + 1) * F]

        where:
            -> f_k: The amount of relevant fodder available in cell k,
                    given by the method 'relevant_fodder()';
            -> n_k: The number of animals of the same species in cell k;
            -> F: The 'appetite' of the animal.

        Parameters:
        ----------
            migrating_specie: str
                String with 'Herbivore' or 'Carnivore';

            neighbour: <class 'type'>
                The landscape neighbour object.

        Returns:
        ----------
            Int with the relative abundance of a given specie.
        """
        f_k = neighbour.relevant_fodder(migrating_specie, neighbour)
        n_k = len(neighbour.population[migrating_specie] +
                  neighbour.new_population[migrating_specie])

        if migrating_specie is 'Herbivore':
            return f_k / ((n_k + 1) * Herbivore.parameters['F'])
        else:
            return f_k / ((n_k + 1) * Carnivore.parameters['F'])

    @staticmethod
    def relevant_fodder(migrating_specie, neighbour):
        """This is the relevant fodder (f_k) that is used to calculated
        the relative abundance in the method 'relative_abundance()'.

        Formula and conditions:
        ----------
            -> The amount of plant fodder available if the migrating
                animal is 'Herbivore';
            -> The total weight of all herbivores in cell k if the
                migrating animal is 'Carnivore'.

        Parameters:
        ----------
            migrating_specie: str
                String with 'Herbivore' or 'Carnivore';

            neighbour: <class 'type'>
                The landscape neighbour object.

        Returns:
        ----------
            Int with the relevant fodder of a give specie.
        """
        if migrating_specie is 'Herbivore':
            return neighbour.fodder
        elif migrating_specie is 'Carnivore':
            f_k = 0
            herbivores = neighbour.population['Herbivore']
            migrated_herbivores = neighbour.new_population['Herbivore']

            for herbivore in herbivores + migrated_herbivores:
                f_k += herbivore.weight

            return f_k

    @classmethod
    def check_unknown_parameters(cls, params):
        """This method checks any unknown parameter given by the user
        and raises a ValueError if necessary.

        Parameter:
        ----------
            params: list
                List with the landscape's parameters.
        """
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def check_non_negative_parameters(cls, param_key, params):
        """This method checks any non-negative parameter given by the
        user and raises a ValueError if necessary.

        Parameters:
        ----------
            param_key: str
                String with the parameter key;

            params: list
                List with the landscape's parameters.
        """
        if params[param_key] < 0:  # check here and others restrictions
            raise ValueError("The parameter *{}* must be "
                             "non-negative".format(param_key))

    @classmethod
    def set_parameters(cls, params):
        """This method sets the parameter for the landscapes.

        Parameter:
        ----------
            params: list
                List with the landscape's parameters.
        """
        cls.check_unknown_parameters(params)
        cls.check_non_negative_parameters('f_max', params)
        cls.parameters.update(params)

    def __init__(self):
        """Constructor for the landscape cells."""
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.new_population = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    def herbivore_feed(self):
        """This method organizes the population of herbivores in order
        of greatest fitness (those who eat first) to worst. Then,
        per animal, it is applied the herbivore eating rules,
        as following:

        Formula and conditions:
        ----------
            -> 'F': Animal´s appetite;
            -> 'f': Available amount of fodder.
            -> if 'F' <= 'f', then the animal eats 'F';
            -> elif 0 < 'f' < 'F', then the animal eats 'f' - 'F';
            -> elif 'f' = 0, then the animal does not eat.
        """
        self.population['Herbivore'].sort(key=lambda h: h.fitness,
                                          reverse=True)
        for herbivore in self.population['Herbivore']:
            amount_eaten = 0
            h_appetite = herbivore.parameters["F"]
            available_fodder = self.fodder
            if h_appetite <= available_fodder:
                available_fodder -= h_appetite
                amount_eaten += h_appetite
            elif 0 < available_fodder < h_appetite:
                available_fodder = 0
                amount_eaten += h_appetite - available_fodder
            herbivore.gain_weight(amount_eaten)
            self.fodder = available_fodder

    def carnivore_feed(self):
        """This method organizes the population of carnivore in order
        of greatest fitness (those who eat first) to worst. Then,
        organizes the population of herbivore in order of worst fitness
        (those who are hunt first) to greatest. Then, per each animal,
        it is applied the carnivore eating rules, as following:

        Formula and conditions:
        ----------
            -> Carnivores prey on herbivores on Jungle, Savannah and
               Desert landscapes, and do not prey on each oder;
            -> A carnivore tries to kill a herbivore per time, beginning
               with the herbivore with worst fitness, and then to the
               next herbivore until has eaten an amount 'F' of
               herbivore weight;
            -> The probability to kill a herbivore is given by the method
               'will_kill()';
            -> The carnivore weight increases by the method
               'gain_weight()' which also updates its fitness;
            -> Every herbivore killed is removed from the population
               by the python's built-in method '.remove()'.
        """
        for carnivore in self.population['Carnivore']:
            self.population['Herbivore'] = carnivore.eat_herb(
                self.population['Herbivore'])

    def add_newborns(self):
        """This method extend a specie population adding their
        offspring."""
        for species in self.population.values():
            newborns = []
            for animal in species:
                if animal.birth(len(species)):
                    newborn = type(animal)()
                    animal.update_weight_after_birth(newborn.weight)
                    newborns.append(newborn)
            species.extend(newborns)

    def migrate(self, neighbours):
        """This method carries out the migration of the island,
        according to the followings:

        Formula and conditions:
        ----------
            -> The animals migrate ate least once a year;
            -> The migration depends on animals fitness and availability
               of fodder in the neighboring cells;
            -> Animals can only move to north, south, west and east,
               according to the cells provided by the method
               'neighbour_cells()';
            -> The decision to move is given by the method 'will_move()';
            -> The propensity of an animal to move to a habitable
               neighbour is given by the method 'propensities()';
            -> The propensities depends on the 'Relevant fodder' and
               'Relative abundance' given by the methods
               'relevant_fodder()' and 'relative_abundance()',
               respectively;
            -> The cumulative probabilities is given by the method
                'cumsum()';
            -> The decision of migrating to a specifically neighbour
               is given when the 'np.random.random()' number is equal
               or lager then the cumulative probability.
        """
        for migrating_specie, animals in self.population.items():
            if len(neighbours) > 0 and len(animals) > 0:
                for animal in animals:
                    cum_prob = self.cumsum(migrating_specie,
                                           neighbours)
                    if animal.will_migrate():
                        n = 0
                        while np.random.random() >= cum_prob[n]:
                            n += 1
                        neighbours[n].new_population[
                            migrating_specie].append(animal)
                        self.population[migrating_specie].remove(animal)

    def add_new_migrated(self):
        """This method adds the migrated animals to the population of
        each landscape cell, according to its specie, and empty the
        list in 'new_population', also according to its specie."""
        for species in self.population.keys():
            specie_list = self.new_population[species]
            self.population[species].extend(specie_list)
            self.new_population[species] = []

    def get_old(self):
        """This method identifies each specie of animals and communicates
        to the method 'get_old()' in fauna in order to apply the aging
        for each animal."""
        for specie_objects in self.population.values():
            for animal in specie_objects:
                animal.get_old()

    def lose_weight(self):
        """This method identifies each specie of animals and communicates
        to the method 'lose_weight()' in fauna in order to apply the
        weight loss for each animal."""
        for specie_objects in self.population.values():
            for animal in specie_objects:
                animal.lose_weight()

    def die(self):
        """This method determines if an animal will die according to
        the probability in the method 'will_die()' in fauna."""
        for specie_type in self.population.keys():
            survivors = []
            for animal in self.population[specie_type]:
                if not animal.will_die():
                    survivors.append(animal)
            self.population[specie_type] = survivors


class Jungle(Cells):
    """The jungle landscape cells offer fodder for Herbivores and
    Carnivores can prey on Herbivore in this cell."""
    parameters = {'f_max': 800.0, 'alpha': None}

    def __init__(self):
        """Constructor for the desert."""
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder growth from the
        previous year to now and then calls the methods
        'herbivore_feed()' and 'carnivore_feed()', respectively,
        in order to execute the animals eating conditions and rules.

        Formula and conditions:
        ----------
            -> The yearly amount of fodder in the jungle landscape
               cells is always restored to the max ('f_max'):

        'f' = 'f_max'

        where :
            -> 'f_max': The maximum possible amount of fodder in
                        the landscape;
            -> 'f':     The remainder available amount of fodder
                        from previous year..
        """
        self.fodder = self.parameters['f_max']
        self.herbivore_feed(), self.carnivore_feed()


class Savannah(Cells):
    """The savannah landscape cells offer fodder for Herbivores,
    but in limited quantity and sensitive to overgrazing. Carnivores
    can prey on Herbivore in this cell."""
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        """Constructor for the desert."""
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder growth from the
        previous year to now and then calls the methods
        'herbivore_feed()' and 'carnivore_feed()', respectively,
        in order to execute the animals eating conditions and rules.

        Formula and conditions:
        ----------
            -> The yearly amount of fodder in the savannah landscape
               cells is always calculated by the following formula:

        'alpha' * ('f_max' - f)

        where :
            -> 'alpha': The growth rate of fodder;
            -> 'f_max': The maximum possible amount of fodder in
                        the landscape;
            -> 'f':     The remainder available amount of fodder
                        from previous year.
        """
        alpha = self.parameters['alpha']
        f_max = self.parameters['f_max']
        f = self.fodder
        self.fodder += alpha * (f_max - f)
        self.herbivore_feed(), self.carnivore_feed()


class Desert(Cells):
    """The desert landscape cells receives animals, but there is no
    fodder available for the animal Herbivore. Although Carnivores can
    prey on Herbivore in this cell."""

    def __init__(self):
        """Constructor for the desert."""
        super().__init__()

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder growth,
        although, for desert landscape cells, there is no fodder
        growth, then fodder is always equal to zero."""
        self.fodder = 0
        self.herbivore_feed(), self.carnivore_feed()


class Ocean(Cells):
    """Passive cells of this type, because, in this project,
    the landscape ocean does not receive the animals neither
    Herbivore or Carnivore."""

    def __init__(self):
        """Constructor for the ocean."""
        super().__init__()


class Mountain(Cells):
    """Passive cells of this type, because, in this project,
    the landscape mountain does not receive the animals neither
    Herbivore or Carnivore."""

    def __init__(self):
        """Constructor for the mountain."""
        super().__init__()

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
            migrating_specie: str: <class 'Herbivore'>, or
                                   <class 'Carnivore'>

            neighbours: list: i.e. [Jungle, Savannah, ...]

        Returns:
        ----------
            List with probabilities.
        """
        propensities = [neighbour.propensity(migrating_specie, neighbour)
                        for neighbour in neighbours]

        prob = [propensity / sum(propensities)
                for propensity in propensities]

        return np.cumsum(prob)

    @staticmethod
    def propensity(migrating_specie, neighbour):
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
            migrating_specie: str: <class 'Herbivore'>, or
                                              <class 'Carnivore'>

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
            migrating_specie: str: <class 'Herbivore'>, or
                                              <class 'Carnivore'>

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
            migrating_specie: str: <class 'Herbivore'>, or
                                              <class 'Carnivore'>

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

    @classmethod  # tested
    def check_unknown_parameters(cls, params):
        """This method checks any unknown parameter given by the user."""
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod  # tested
    def check_non_negative_parameters(cls, param_key, params):
        """This method checks any non-negative parameter given by the
        user."""
        if params[param_key] < 0:  # check here and others restrictions
            raise ValueError("The parameter *{}* must be "
                             "non-negative".format(param_key))

    @classmethod
    def set_parameters(cls, params):  # tested
        """This method sets the parameter for the landscapes."""
        cls.check_unknown_parameters(params)
        cls.check_non_negative_parameters('f_max', params)
        cls.parameters.update(params)

    def __init__(self):
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.new_population = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    def herbivore_feed(self):  # tested
        """This method organizes the population of herbivores in order
        of greatest fitness (those who eat first) to worst. Then,
        per animal (herb_object), it is applied the herbivore eating
        rules, as following:

        * Notations:    F:  Animal´s appetite
                        f:  Available amount of fodder.

        * rules:        1.  if F <= f:          f - F
                                                w = w + ('beta' * F)
                        2. elif 0 < f < F:      f = 0
                                                w = 'beta' * (F - f)
                        3. else                 f = 0
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
        (those who are eaten first) to greatest. Then, per animal
        (carn_object), it is applied the carnivore eating rules,
        as following:

        1. Carnivores prey on herbivores on Jungle, Savannah and Desert
        landscapes, but do not prey on each oder;
        2. A carnivore tries to kill a herbivore per time, beginning
        with the herbivore with worst fitness, and then to the next
        herbivore until has eaten an amount 'F' of herbivore weight;
        3. The probability to kill a herbivore is given by the method
        'is_herb_killed(h_fitness)';
        4. Every herbivore killed is removed from the population by the
        python's built-in method '.remove()';
        5. The carnivore weight increases by the method
        'gain_weight(h_weight)';
        6. The carnivore fitness is updated every time he eats, by the
        method 'update_fitness()'.
        """
        self.population['Carnivore'].sort(key=lambda h: h.fitness,
                                          reverse=True)

        self.population['Herbivore'].sort(key=lambda h: h.fitness)

        for carnivore in self.population['Carnivore']:
            appetite = carnivore.parameters['F']
            amount_eaten = 0

            for herbivore in self.population['Herbivore']:

                if amount_eaten >= appetite:
                    break

                elif carnivore.will_kill(herbivore.fitness):
                    food_wanted = appetite - amount_eaten

                    if herbivore.weight <= food_wanted:
                        amount_eaten += herbivore.weight
                        self.population['Herbivore'].remove(herbivore)

                    elif herbivore.weight > food_wanted:
                        amount_eaten += food_wanted
                        self.population['Herbivore'].remove(herbivore)

            carnivore.gain_weight(amount_eaten)

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

        1. The animals migrate ate least once a year;
        2. The migration depends on animals fitness and availability of
        fodder in the neighboring cells;
        3. Animals can only move to north, south, west and east,
        according to the cells provided by the method
        'neighbour_cells()';

        -> The decision to move is given by the method 'will_move()';
        -> The propensity of an animal to move to each habitable
        neighbour is given by the method 'propensities()';

        -> The decision of each neighbour to move is given by the method
        'xxxx()'


        5. If the animals move, this also depends on the amount of
        fodder available in the neighboring cells, which is calculated
        by the relative abundance of fodder defined in the method
        'relative_abundance()'. Relevant fodder is the amount of plant
        available if the moving animal is a herbivore, and the total
        weight of all herbivores in cell k if the moving animal is a
        carnivore.
        6. The propensity to move from i to j in the neighbour is
        given by the method 'propensity()'.
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
        each landscape cell."""
        for species in self.population.keys():
            specie_list = self.new_population[species]
            self.population[species].extend(specie_list)
            self.new_population[species] = []

    def get_old(self):  # tested
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
    parameters = {'f_max': 800.0, 'alpha': None}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder grown** in
        the previous year and then calls the methods 'herbivore_feed()'
        and 'carnivore_feed()', respectively, in order to execute the
        animals eating conditions and rules

        ** Notes: The yearly amount of fodder in the Jungle landscape
        is always returned to its maximum, given by the parameter_key
        'f_max'.
        """
        self.fodder = self.parameters['f_max']
        self.herbivore_feed(), self.carnivore_feed()


class Savannah(Cells):
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder grown** in
        the previous year and then calls the methods 'herbivore_feed()'
        and 'carnivore_feed()', respectively, in order to execute the
        animals eating conditions and rules

        ** Notes: The yearly amount of fodder in the Savannah landscape
        is always calculated by the following formula:

        * Formula = 'alpha' * ('f_max' - f)

            where   'alpha':    The growth rate of fodder;
                    'f_max':    The maximum possible amount of fodder in
                                the landscape;
                    'f':        The remainder available amount of fodder
                                from previous year.
        """
        alpha = self.parameters['alpha']
        f_max = self.parameters['f_max']
        self.fodder += alpha * (f_max - self.fodder)
        self.herbivore_feed(), self.carnivore_feed()


class Desert(Cells):
    def __init__(self):
        super().__init__()

    def grow_fodder_and_feed(self):
        """This method increases the amount of fodder grown** in
        the previous year and then calls the methods 'herbivore_feed()'
        and 'carnivore_feed()', respectively, in order to execute the
        animals eating conditions and rules

        ** Notes: There is no fodder growth in the desert landscape.
        """
        self.fodder = 0
        self.herbivore_feed(), self.carnivore_feed()


class Ocean(Cells):
    def __init__(self):
        super().__init__()


class Mountain(Cells):
    def __init__(self):
        super().__init__()

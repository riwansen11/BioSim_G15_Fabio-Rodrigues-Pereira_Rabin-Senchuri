# -*- coding: utf-8 -*-
import random
import numpy as np
from src.biosim.fauna import Herbivore, Carnivore

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Cells:
    parameters = {}

    @staticmethod
    def relevant_abundance(animal_number, appetite,
                           relevant_fodder):
        return relevant_fodder / ((animal_number + 1) * appetite)

    @classmethod  # tested
    def check_unknown_parameters(cls, params):
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod  # tested
    def check_non_negative_parameters(cls, param_key, params):
        if params[param_key] < 0:  # check here and others restrictions
            raise ValueError("The parameter *{}* must be "
                             "non-negative".format(param_key))

    @classmethod
    def set_parameters(cls, params):  # tested
        cls.check_unknown_parameters(params)
        cls.check_non_negative_parameters('f_max', params)
        cls.parameters.update(params)

    def __init__(self):
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.new_population = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    '''def sort_animals_by_fitness(self, specie, decreasing=False):  # ok
        """This method sorts the population of a given specie. There
        are 2 types of sorting, with increasing values of fitness
        (decreasing=False) or decreasing values of fitness
        (decreasing=True).

        :param  specie:     string: 'Herbivore' or 'Carnivore'
        :param  decreasing: bol:    True for decreasing fitness values;
                                    False for increasing fitness values;
        """
        fitness, animals = [], []
        for animal in self.population[specie]:
            fitness.append(animal.fitness)
            animals.append(animal)

        animals_by_decreasing_fitness = dict(zip(fitness, animals))

        sorted_stronger_weaker_herbivores = \
            [animals_by_decreasing_fitness[i] for i in
             sorted(animals_by_decreasing_fitness.keys(),
                    reverse=decreasing)]

        self.population[specie] = sorted_stronger_weaker_herbivores'''

    def herbivore_feed(self):  # tested
        """This method organizes the population of herbivores in order
        of greatest fitness (those who eat first) to worst. Then,
        per animal (herb_object), it is applied the herbivore eating
        rule, as following:

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
        for herb_object in self.population['Herbivore']:
            h_ate = 0
            h_appetite = herb_object.parameters["F"]
            available_fodder = self.fodder
            if h_appetite <= available_fodder:
                available_fodder -= h_appetite
                h_ate += h_appetite
            elif 0 < available_fodder < h_appetite:
                available_fodder = 0
                h_ate += h_appetite - available_fodder
            # gain weight
            herb_object.gain_weight(h_ate)
            # update fitness
            herb_object.update_fitness()
            # set new amount of fodder available
            self.fodder = available_fodder

    def carnivore_feed(self):
        self.population['Carnivore'].sort(key=lambda h: h.fitness,
                                          reverse=True)
        self.population['Herbivore'].sort(key=lambda h: h.fitness)
        for carn_object in self.population["Carnivore"]:
            c_ate = 0
            c_appetite = carn_object.parameters['F']
            c_food_desired = c_appetite - c_ate
            # print(c_ate, c_appetite, c_food_desired)
            # print(self.population['Herbivore'])

            for herb_object in self.population['Herbivore']:
                h_fitness = herb_object.fitness
                h_weight = herb_object.weight
                is_herb_killed = carn_object.is_herb_killed(h_fitness)
                # print(is_herb_killed, c_food_desired, 'lalala')
                if c_food_desired <= 0:
                    # print(c_food_desired <= 0)
                    break
                elif is_herb_killed:
                    # print('is_killed', is_herb_killed)
                    if h_weight <= c_food_desired:
                        carn_object.gain_weight(h_weight)
                        carn_object.update_fitness()
                        c_ate += h_weight
                        self.population["Herbivore"].remove(herb_object)
                    else:
                        carn_object.gain_weight(c_food_desired)
                        carn_object.update_fitness()
                        c_ate += c_food_desired
                        self.population["Herbivore"].remove(herb_object)

    def get_old(self):  # tested
        """This method identifies each specie of animals and communicates
        to the method 'get_old()' in fauna in order to apply the aging
        for each animal (pop_object)"""
        for specie_objects in self.population.values():
            for pop_object in specie_objects:
                pop_object.get_old()

    def lose_weight(self):
        """This method identifies each specie of animals and communicates
        to the method 'lose_weight()' in fauna in order to apply the
        weight loss for each animal (pop_object)"""
        for specie_objects in self.population.values():
            for pop_object in specie_objects:
                pop_object.lose_weight()

    def add_newborns(self):
        for specie_objects in self.population.values():
            newborns = []
            for animal_object in specie_objects:
                if animal_object.birth(len(specie_objects)):
                    newborn = type(animal_object)()
                    animal_object.update_weight_after_birth(
                        newborn.weight)
                    newborns.append(newborn)
            specie_objects.extend(newborns)

    # def migrate(self, neighbour_cells):
    #
    #     for species, animals in self.population.items():
    #         if animals:
    #             neighbour_cell_props = [neighbour.neighbour_cell_propensity(species) for neighbour in
    #                                     neighbour_cells]
    #
    # def neighbour_cell_propensity(self, species):
    #     relevant_fodder = self.fodder if species == "Herbivore" \
    #         else self.total_herbivore_mass()
    #     r_abundance = self.relevant_abundance(len(self.population[species]),
    #                                           self.population[species][0].parameters["F"],
    #                                           relevant_fodder)
    #     return np.exp(species.default_params["lambda"] * r_abundance)
    # def relative_abundance():
    #     return self.fodder / ((len(self.population[specie]) + 1) *
    #                      Herbivore.parameters["F"])
    #
    # def carnivore_fodder(self, specie):
    #     return self.total_herbivore_mass() / ((len(self.population[specie]) + 1) *
    #                      Carnivore.parameters["F"])

    def propensity(self, specie):
        num_animals = len(self.population[specie]) + len(
            self.new_population[specie])
        if specie == "Herbivore":
            appetite = Herbivore.parameters['F']
        else:
            appetite = Carnivore.parameters['F']

        relevant_fodder = self.fodder if specie == "Herbivore" else \
            self.total_herbivore_mass()
        relative_abundance = self.relevant_abundance(num_animals,
                                                     appetite,
                                                     relevant_fodder)
        if specie == "Herbivore":
            return np.exp(Herbivore.parameters['lambda'] *
                          relative_abundance)
        else:
            return np.exp(Carnivore.parameters['lambda'] *
                          relative_abundance)

        # carnivore_propensity = np.exp(
        #     Carnivore.parameters["lambda"] *
        #     self.carnivore_fodder(specie))
        #
        # return tuple([herbivore_propensity, carnivore_propensity])

    def propensity_list(self, species, neighbour_cells):
        # if species == "Herbivore":

        propensities = [cell.propensity(species)
                        for cell in neighbour_cells]
        probability_list = [propensity / np.sum(propensities)
                            for propensity in propensities]
        # else:
        #     propensities = [cell.propensity(animals)
        #                     for cell in neighbour_cells]
        #     probability_list = [propensity / np.sum(propensities)
        #                         for propensity in propensities]
        return probability_list

    def migrate(self, neighbour_cell):
        for species, animals in self.population.items():
            if len(animals) > 0:
                probability_list = self.propensity_list(
                    species, neighbour_cell)
                cumulative_probability = np.cumsum(probability_list)
                migrated_animals = []
                for animal in animals:
                    if animal.migration_chances():
                        # self.choose_migration_cell(
                        #   animal, neighbour_cells, probability_list)
                        rand_num = random.random()
                        n = 0
                        while rand_num >= cumulative_probability[n]:
                            n += 1
                        neighbour_cell[n].new_population[species].append(
                            animal)
                        migrated_animals.append(animal)
                self.population[species] = [animal for animal in animals
                                            if animal not in
                                            migrated_animals]

    def die(self):
        for specie_type in self.population.keys():
            survivors = []
            for animal_object in self.population[specie_type]:
                if not animal_object.die():
                    survivors.append(animal_object)
            self.population[specie_type] = survivors

    def total_herbivore_mass(self):
        herb_mass = 0
        for herb in self.population['Herbivore']:
            herb_mass += herb.weight
        return herb_mass


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
        print('f_max:', self.fodder)
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
        f = self.fodder
        if f is not f_max:  # means not first year of the simulation
            self.fodder += alpha * (f_max - f)
        print(alpha, f_max, f)
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

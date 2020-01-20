# -*- coding: utf-8 -*-
from src.biosim.fauna import Herbivore, Carnivore
import numpy as np
import random

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
    def set_parameters(cls, params):
        cls.check_unknown_parameters(params)
        cls.check_non_negative_parameters('f_max', params)
        cls.parameters.update(params)

    def __init__(self):
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.new_population = {'Herbivore': [], 'Carnivore': []}
        self.fodder = 0

    def herbivore_feed(self):
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

            herb_object.gain_weight(h_ate)
            self.fodder = available_fodder

    def carnivore_feed(self):
        self.population['Carnivore'].sort(key=lambda h: h.fitness,
                                         reverse=True)
        self.population['Herbivore'].sort(key=lambda h: h.fitness)

        for carnivore in self.population['Carnivore']:
            appetite = carnivore.parameters['F']
            food_intake = 0
            survivors = []
            for idx, herbivore in enumerate(
                    self.population['Herbivore']):
                if food_intake >= appetite:
                    survivors.extend(
                        self.population['Herbivore'][idx:])
                    break
                elif carnivore.is_herb_killed(herbivore.fitness):
                    desired_amount = appetite - food_intake
                    if herbivore.weight <= desired_amount:
                        food_intake += herbivore.weight
                    elif herbivore.weight > desired_amount:
                        food_intake += desired_amount
                else:
                    survivors.append(herbivore)
            carnivore.weight += carnivore.parameters['beta'] * food_intake
            carnivore.update_fitness()
            self.population['Herbivore'] = survivors

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

    def propensity(self, specie):
        num_animals = len(self.population[specie]) + len(
            self.new_population[specie])
        if specie == "Herbivore":
            appetite = Herbivore.parameters['F']
        else:
            appetite = Carnivore.parameters['F']

        relevant_fodder = self.fodder if specie == "Herbivore" else \
            self.total_herbivore_mass()
        relative_abundance = self.relevant_abundance(num_animals, appetite,
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
                        neighbour_cell[n].new_population[species].append(animal)
                        migrated_animals.append(animal)
                self.population[species] = [animal for animal in animals
                                            if animal not in
                                            migrated_animals]

    def add_new_migrated(self):
        """
        Add newly mighrated animals to the cell

        """
        for species in self.population.keys():
            new_pop = self.new_population[species]
            self.population[species].extend(new_pop)
            self.new_population[species] = []

    def get_old(self):  # tested
        for specie_objects in self.population.values():
            for animal_object in specie_objects:
                animal_object.get_old()

    def lose_weight(self):
        for specie_objects in self.population.values():
            for animal_object in specie_objects:
                animal_object.lose_weight()

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
        self.fodder = self.parameters['f_max']  # ****check
        self.herbivore_feed(), self.carnivore_feed()


class Savannah(Cells):
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder_and_feed(self):
        self.fodder += self.parameters['alpha'] \
                       * (self.parameters['f_max'] - self.fodder)
        self.herbivore_feed(), self.carnivore_feed()


class Desert(Cells):
    def __init__(self):
        super().__init__()

    def grow_fodder_and_feed(self):
        self.fodder = 0
        self.herbivore_feed(), self.carnivore_feed()


class Ocean(Cells):
    def __init__(self):
        super().__init__()


class Mountain(Cells):
    def __init__(self):
        super().__init__()

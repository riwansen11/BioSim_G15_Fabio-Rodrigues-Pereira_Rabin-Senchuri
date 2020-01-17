# -*- coding: utf-8 -*-
from src.biosim.fauna import Herbivore, Carnivore
import numpy as np

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Cells:
    parameters = {}

    @staticmethod
    def herbivore_relevant_abundance(animal_number, appetite,
                                     relevant_fodder):
        return relevant_fodder / ((animal_number + 1) * appetite)

    @staticmethod
    def carnivore_relevant_abundance(animal_number, appetite,
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
        self.population['Herbivore'].sort(key=lambda h: h.fitness)
        for herbivore_object in reversed(self.population['Herbivore']):
            if herbivore_object.parameters["F"] <= self.fodder:
                self.fodder -= herbivore_object.parameters["F"]
            elif 0 < self.fodder < herbivore_object.parameters["F"]:
                herbivore_object.herb_eating(self.fodder)
                self.fodder = 0

    def carnivore_feed(self):
        self.population["Herbivore"].sort(key=lambda h: h.fitness)
        self.population["Carnivore"].sort(key=lambda i: i.fitness)

        for carn_object in reversed(self.population["Carnivore"]):
            eaten = carn_object.carn_eating_rule(self.population[
                                                     "Herbivore"])

    def add_newborns(self):
        for specie_objects in self.population.values():
            newborns = []
            for animal_object in specie_objects:
                if animal_object.add_newborns(len(specie_objects)):
                    newborn = type(animal_object)()
                    animal_object.update_weight_after_birth(
                        newborn.weight)
                    newborns.append(newborn)
            specie_objects.extend(newborns)

    def migrate(self, neighbour_cells):
        pass

        '''for species in self.popilation.keys():
            for animal in species:
                if animal:
                    neighbour_cell_props = [neighbour.neighbour_cell_prospensity(animal) for neighbour in
                                            neighbour_cells]
                    print(neighbour_cell_props)'''

    def neighbour_cell_propensity(self, species):
        pass
        '''relevant_fodder = self.fodder if species.__class__.__name__ == "Herbivore" \
            else self.total_herbivore_mass()
        h_relevant_abundance = self.herbivor_relevant_abundance(len(self.animal_pop[0]),
                                                                species.default_params["F"],
                                                                relevant_fodder)
        c_relevant_abundance = self.carnivore_relevant_abundance(len(self.animal_pop[1]),
                                                                 species.default_params["F"],
                                                                 relevant_fodder)
        h_propensity = np.exp(species.default_params["lambda"] * h_relevant_abundance)
        c_propensity = np.exp(species.default_params["lambda"] * c_relevant_abundance)

        return tuple([h_propensity, c_propensity])'''

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
        self.fodder = self.parameters['f_max']
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

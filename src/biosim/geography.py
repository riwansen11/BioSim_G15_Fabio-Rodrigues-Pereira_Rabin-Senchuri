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

    @classmethod
    def check_unknown_parameter(cls, params):
        for parameter in params.keys():
            if parameter not in cls.parameters.keys():
                raise ValueError("Unknown parameter provided: "
                                 "*{}*".format(parameter))

    @classmethod
    def check_non_negative_parameter(cls, param_key, params):
        if params[param_key] < 0:  # check here and others restrictions
            raise ValueError("The parameter *{}* must be "
                             "non-negative".format(param_key))

    @classmethod
    def set_parameters(cls, params):
        cls.check_unknown_parameter(params)
        cls.check_non_negative_parameter('f_max', params)
        cls.parameters.update(params)

    def __init__(self):
        self.population = {Herbivore: [], Carnivore: []}
        self.new_population = {Herbivore: [], Carnivore: []}

    def num_herbs(self):
        """
            Returns
            -------
                int
                    Number of herbivores in each cell
        """
        return len(self.animal_pop[0])

    def num_carn(self):
        """
            Returns
            -------
                int
                    Number of carnivores in each cell
        """
        return len(self.animal_pop[1])

    def total_herbivore_mass(self):
        herb_mass = 0
        for herb in self.animal_pop[0]:
            herb_mass += herb.w
        return herb_mass

    def add_animal(self, animals):
        """Add animal to each cell

            Parameters
            ----------
                animal: list
                    list of animals

        """

        for animal in animals:
            age = animal["age"]
            weight = animal["weight"]
            if animal["species"] is "Herbivore":
                self.animal_pop[0].append(Herbivore(age, weight))
            else:
                self.animal_pop[1].append(Carnivore(age, weight))

    def aging(self):
        """
            Returns
            -------
                int
                    age of each animal

        """
        for animals_species in self.animal_pop:
            for animal in animals_species:
                animal.ages()

    def loose_weight(self):
        """
            Returns
            -------
                int
                    amount of weight lost
        """
        for animals_species in self.animal_pop:
            for animal in animals_species:
                animal.weight_decrease()

    def death(self):
        """
             Returns
             -------
                list
                    Survivors list of animals for each species
        """

        survivors_herb = []
        for animal in self.animal_pop[0]:
            if not animal.death():
                survivors_herb.append(animal)
        self.animal_pop[0] = survivors_herb

        survivors_carn = []
        for animal in self.animal_pop[1]:
            if not animal.death():
                survivors_carn.append(animal)
        self.animal_pop[1] = survivors_carn

    def birth(self):
        """Gives the list of newborn herbivore and carnivore animals

            Returns
            -------
                list
                    list newborn herbivore and carnivore animals

        """
        for animal_species in self.animal_pop:
            newborn_animal = []
            for animal in animal_species:
                if animal.birth(len(animal_species)):
                    newborn = type(animal)()
                    animal.update_weight_after_birth(newborn.weight)
                    newborn_animal.append(newborn)
            animal_species.extend(newborn_animal)

    def herb_feed(self):
        """Gives the amount of food eating by herbivore

            Returns
            -------
                int
                    amount of fodder eaten by herbivore
        """
        self.animal_pop[0].sort(key=lambda a: a.fitness)
        for herb in reversed(self.animal_pop[0]):
            eaten = herb.h_eating_rule(self.fodder)
            self.fodder -= eaten

    def carn_feed(self):
        pass

    def make_migration(self, neighbour_cells):
        for species in self.animal_pop:
            for animal in species:
                if animal:
                    neighbour_cell_props = [neighbour.neighbour_cell_prospensity(animal) for neighbour in
                                            neighbour_cells]
                    print(neighbour_cell_props)

    def neighbour_cell_prospensity(self, species):
        relevant_fodder = self.fodder if species.__class__.__name__ == "Herbivore" \
            else self.total_herbivore_mass()
        h_relevant_abundance = self.herbivor_relevant_abundance(len(self.animal_pop[0]),
                                                                species.default_params["F"],
                                                                relevant_fodder)
        c_relevant_abundance = self.carnivore_relevant_abundance(len(self.animal_pop[1]),
                                                                 species.default_params["F"],
                                                                 relevant_fodder)
        h_propensity = np.exp(species.default_params["lambda"] * h_relevant_abundance)
        c_propensity = np.exp(species.default_params["lambda"] * c_relevant_abundance)

        return tuple([h_propensity, c_propensity])

    @staticmethod
    def herbivor_relevant_abundance(animal_number, appetite, relevant_fodder):
        return relevant_fodder / ((animal_number + 1) * appetite)

    @staticmethod
    def carnivore_relevant_abundance(animal_number, appetite, relevant_fodder):
        return relevant_fodder / ((animal_number + 1) * appetite)


    def procreation(self):
        pass

    def feeding(self):
        pass


class Jungle(Cells):
    default_params = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder = self.parameters['f_max']  # ****check


class Savannah(Cells):
    default_params = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self):
        super().__init__()
        self.fodder = self.parameters['f_max']

    def grow_fodder(self):
        self.fodder += self.parameters['alpha'] * (
                self.parameters['f_max'] - self.fodder)  # ****check


class Desert(Cells):
    def __init__(self):
        super().__init__()


class Ocean(Cells):
    def __init__(self):
        super().__init__()


class Mountain(Cells):
    def __init__(self):
        super().__init__()

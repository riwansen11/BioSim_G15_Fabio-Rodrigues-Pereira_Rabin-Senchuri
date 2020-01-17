# -*- coding: utf-8 -*-
import textwrap
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from src.biosim.fauna import Herbivore, Carnivore

"""
This is the Island model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Island:
    habitable_geos = {'S': Savannah, 'J': Jungle, 'D': Desert}

    fauna_classes = {'Herbivore': Herbivore, 'Carnivore': Carnivore}

    geo_classes = {'O': Ocean, 'S': Savannah, 'M': Mountain,
                   'J': Jungle, 'D': Desert}

    @staticmethod  # tested
    def check_string_instance(argument):
        if not isinstance(argument, str):
            raise TypeError('Argument *{}* must be provided as '
                            'string'.format(argument))

    @staticmethod  # tested
    def check_list_instance(argument):
        if not isinstance(argument, list):
            raise TypeError('Argument *{}* must be provided as '
                            'list'.format(argument))

    @staticmethod  # tested
    def check_dict_instance(argument):
        if not isinstance(argument, dict):
            raise TypeError('Argument *{}* must be provided as '
                            'dictionary'.format(argument))

    @staticmethod  # tested
    def list_geo_cells(island_map):
        geos = textwrap.dedent(island_map).splitlines()
        return [list(row.strip()) for row in geos]

    @staticmethod  # tested
    def check_invalid_line_lengths(geos):
        length_count = [len(row) for row in geos]
        for i in length_count:
            if i is not length_count[0]:
                raise ValueError('Different line lengths detected')

    @staticmethod  # tested
    def check_invalid_boundary(geos):
        for north in geos[0]:
            for south in geos[-1]:
                if north is not 'O' or south is not 'O':
                    raise ValueError('The boundary is not Ocean')
        for row in geos:
            west, east = row[0], row[-1]
            if west is not 'O' or east is not 'O':
                raise ValueError('The boundary is not Ocean')

    @classmethod  # tested
    def check_invalid_character(cls, geos):
        for row in geos:
            for letter in row:
                if letter not in cls.geo_classes.keys():
                    raise ValueError('Invalid character identified')

    @classmethod
    def check_coordinates_exists(cls, coordinates, cells):
        cls.check_dict_instance(cells)
        if coordinates not in cells.keys():
            raise ValueError('These *{}* coordinates are not '
                             'found'.format(coordinates))

    @classmethod
    def check_habitability(cls, coordinates, cells):
        cls.check_dict_instance(cells)
        if type(cells[coordinates]) not in \
                cls.habitable_geos.values():
            raise TypeError('This *{}* area is not '
                            'habitable'.format(coordinates))

    def __init__(self, island_map):
        self.geos = self.list_geo_cells(island_map)
        self.check_invalid_line_lengths(self.geos)
        self.check_invalid_boundary(self.geos)
        self.check_invalid_character(self.geos)
        self.cells = self.create_cells()

    def create_cells(self):
        loc = [(i, j) for i in range(len(self.geos))
               for j in range(len(self.geos[0]))]
        geo = [self.geo_classes[geo]() for j in range(len(self.geos))
               for geo in self.geos[j]]
        return dict(zip(loc, geo))

    @property
    def habitable_cells(self):
        coordinates, geo_objects = [], []
        for coordinate, geo_object in self.cells.items():
            if type(geo_object) in self.habitable_geos.values():
                coordinates.append(coordinate)
                geo_objects.append(geo_object)
        return dict(zip(coordinates, geo_objects))

    def set_parameters(self, param_key, params):
        self.check_string_instance(param_key)
        self.check_dict_instance(params)
        merged_classes = dict(**self.fauna_classes, **self.geo_classes)
        merged_classes[param_key].set_parameters(params)

    def add_population(self, given_pop):
        self.check_list_instance(given_pop)
        for population in given_pop:
            coordinate = population['loc']
            self.check_coordinates_exists(coordinate, self.cells)
            self.check_habitability(coordinate, self.cells)
            individual_objects = []
            for individual in population['pop']:
                species = individual['species']
                age = individual['age']
                weight = individual['weight']
                individual_object = \
                    self.fauna_classes[species](age, weight)

                individual_objects.append(individual_object)
            geo_object = self.cells[coordinate]
            for animal_object in individual_objects:
                geo_object.population[
                    type(animal_object).__name__].append(animal_object)

    def neighbour_cell(self, loc):  # returns the habitable geo_objects
        neighbours = [(loc[0], loc[1] - 1),
                      (loc[0] - 1, loc[1]),
                      (loc[0] + 1, loc[1]),
                      (loc[0], loc[1] + 1)]
        return [self.habitable_cells[coordinates] for coordinates in
                neighbours if coordinates in self.habitable_cells.keys()]

    def yearly_cycle(self):
        for coordinate, geo_object in self.habitable_cells.items():
            geo_object.feed()
            geo_object.add_newborns()
            # neighbour_cell = self.neighbour_cell(coordinate)
            # geo_object.migrate(neighbour_cell)
            geo_object.get_old()
            geo_object.lose_weight()
            geo_object.die()

    def get_population_numbers(self):
        population = {'Coordinates': [], 'Herbivore': [],
                      'Carnivore': []}
        for location, geo_object in self.cells.items():
            population['Coordinates'].append(location)
            population['Herbivore'].append(len(geo_object.population[
                                            'Herbivore']))
            population['Carnivore'].append(len(geo_object.population[
                                            'Carnivore']))
        return population

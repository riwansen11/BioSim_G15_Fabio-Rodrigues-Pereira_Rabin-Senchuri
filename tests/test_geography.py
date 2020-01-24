# -*- coding: utf-8 -*-

"""
This is the geography pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
import random as rd
from biosim.simulation import BioSim
from biosim.geography import Jungle, Savannah
import numpy as np


def test_check_unknown_parameters():
    """Test method 'check_unknown_parameters()' if it does not
    identifies the given parameter and returns ValueError"""
    with pytest.raises(ValueError):
        Jungle.check_unknown_parameters(params={'f_min': 100})
        Savannah.check_unknown_parameters(params={'f_min': 100})


def test_check_known_parameters():
    """Test method 'check_unknown_parameters()' if it identifies the
    given parameter and does not return ValueError"""
    Jungle.check_unknown_parameters(params={'f_max': 100})
    Savannah.check_unknown_parameters(params={'f_max': 100})


def test_now_negative_parameters():
    """Test method 'check_non_negative_parameters(param_key, params)'
    if it identifies the negative value of a given parameter and returns
    ValueError"""
    param_key, params = 'f_max', {'f_max': 1}
    Jungle.check_non_negative_parameters(param_key, params)
    Savannah.check_non_negative_parameters(param_key, params)


def test_animal_got_old():
    """Test if the method 'get_old()' correctly increases in 1 year all
    the animal_objects stored in a specific geo_object"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                    {"species": "Herbivore", "age": 2, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    geo_object = t.island.habitable_cells[loc]
    herb_object_1 = geo_object.population['Herbivore'][0]
    herb_object_2 = geo_object.population['Herbivore'][1]
    herb_young_1 = herb_object_1.age
    herb_young_2 = herb_object_2.age
    geo_object.get_old()
    herb_older_1 = herb_object_1.age
    herb_older_2 = herb_object_2.age
    assert herb_older_1 is (herb_young_1 + 1)
    assert herb_older_2 is (herb_young_2 + 1)


def test_herbivore_feed():
    """Many testes for the method 'herbivore_feed()':
    1. if the fodder reduces when a animal eats it.
    2. if the weight of the animal increases after eat.
    3. if the fitness of the animal updates after eat.
    """
    island_map = "OOO\nOJO\nOOO"
    ini_pop = [
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 10, "weight": 10}]}]
    t = BioSim(island_map, ini_pop, None)
    loc = (1, 1)
    previous_fodder = t.island.cells[loc].fodder
    previous_herbivore_weight = t.island.cells[loc].population[
        'Herbivore'][0].weight
    previous_herbivore_fitness = t.island.cells[loc].population[
        'Herbivore'][0].fitness
    t.island.cells[loc].herbivore_feed()
    afterwards_fodder = t.island.cells[loc].fodder
    afterwards_herbivore_weight = t.island.cells[loc].population[
        'Herbivore'][0].weight
    afterwards_herbivore_fitness = t.island.cells[loc].population[
        'Herbivore'][0].fitness
    assert previous_fodder > afterwards_fodder
    assert previous_herbivore_weight < afterwards_herbivore_weight
    assert previous_herbivore_fitness is not afterwards_herbivore_fitness


def test_carnivore_feed():
    """Many testes for the method 'carnivore_feed()':
    1. Test carnivore weight increases after feeding herbivore
    """
    island_map = "OOO\nOJO\nOOO"
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 40}
                for _ in range(40)
            ],
        }
    ]
    t = BioSim(island_map, ini_herbs, None)
    t.add_population(ini_carns)
    loc = (1, 1)
    cell_object = t.island.cells[loc]
    carn_start_weight = np.sum(
        carn.weight for carn in cell_object.population['Carnivore'])
    cell_object.carnivore_feed()
    carn_new_weight = np.sum(
        carn.weight for carn in cell_object.population['Carnivore'])

    assert carn_start_weight < carn_new_weight


def test_animal_number_increases_after_birth():
    """
    Test that the number of animals in the cell increases
    after birth
    """
    island_map = "OOO\nOJO\nOOO"
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 40}
                for _ in range(150)
            ],
        }
    ]
    t = BioSim(island_map, ini_herbs, None)
    loc = (1, 1)
    cell_object = t.island.cells[loc]
    before_birth_total_animal = len(cell_object.population['Carnivore'])
    cell_object.add_newborns()

    assert len(cell_object.population[
                   'Carnivore']) - before_birth_total_animal > 0


def test_animal_death():
    island_map = "OOO\nOJO\nOOO"
    ini_herbs = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5,
                 "weight": rd.randint(1, 5)}
                for _ in range(150)
            ],
        }
    ]
    ini_carns = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 5,
                 "weight": rd.randint(1, 5)}
                for _ in range(40)
            ],
        }
    ]
    t = BioSim(island_map, ini_herbs, None)
    t.add_population(ini_carns)
    loc = (1, 1)
    cell_object = t.island.cells[loc]
    cell_object.die()
    assert len(cell_object.population["Carnivore"]) < 40
    assert len(cell_object.population["Herbivore"]) < 150


def test_animal_loose_weight():
    """Test if the method 'lose_weight()' correctly looses the weight
    of the animal"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                    {"species": "Herbivore", "age": 2, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    geo_object = t.island.habitable_cells[loc]
    herb_object_1 = geo_object.population['Herbivore'][0]
    herb_object_2 = geo_object.population['Herbivore'][1]
    before_weight_herb1 = herb_object_1.weight
    before_weight_herb2 = herb_object_2.weight
    geo_object.lose_weight()
    after_weight_herb1 = herb_object_1.weight
    after_weight_herb2 = herb_object_2.weight
    assert before_weight_herb1 > after_weight_herb1
    assert before_weight_herb2 > after_weight_herb2


def test_migration():
    """This tests the migration method checking if the animals have
    moved to the all 4th neighbour cells."""
    island_map = "OOOOO\nOMJMO\nOJDJO\nOMJMO\nOOOOO"
    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": np.random. randint(1, 5),
                 "weight": np.random.randint(20, 40)}
                for _ in range(1000)], }]

    t, loc = BioSim(island_map, ini_pop, 1), (2, 2)

    for k, v in t.island.habitable_cells.items():
        v.migrate(t.island.neighbour_cells(k))

    for k, v in t.island.habitable_cells.items():
        v.add_new_migrated()

    north_neighbour = t.island.cells[(1, 2)].population['Herbivore']
    south_neighbour = t.island.cells[(3, 2)].population['Herbivore']
    west_neighbour = t.island.cells[(2, 1)].population['Herbivore']
    east_neighbour = t.island.cells[(2, 3)].population['Herbivore']

    assert north_neighbour is not 0
    assert south_neighbour is not 0
    assert west_neighbour is not 0
    assert east_neighbour is not 0

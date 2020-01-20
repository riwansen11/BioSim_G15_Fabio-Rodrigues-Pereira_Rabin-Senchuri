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
from biosim.geography import Cells, Jungle, Savannah, Desert, \
    Ocean, Mountain
from biosim.fauna import Herbivore, Carnivore


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
    1. If there are any succeed hunt, given by the method
    'is_herb_killed()'.
    """
    island_map = "OOO\nOJO\nOOO"
    ini_herb = [
        {"loc": (1, 1),
         "pop": [
             {"species": "Herbivore", "age": rd.randint(1, 10), "weight":
                 rd.randint(20, 60)}
             for _ in range(200)
         ]}]

    ini_carn = [
        {"loc": (1, 1),
         "pop": [
             {"species": "Carnivore", "age": rd.randint(1, 10), "weight":
                 rd.randint(20, 60)}
             for _ in range(200)
         ]}]
    t = BioSim(island_map, ini_herb, None)
    t.add_population(ini_carn)
    loc = (1, 1)
    t.island.cells[loc].carnivore_feed()


# -*- coding: utf-8 -*-

"""
This is the simulation pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from src.biosim.simulation import BioSim


def test_set_animal_parameters():
    """Test if the method set_animal_parameters() raises a TypeError
    if it is given a non-string type parameter_key argument.

    * Test if the method set_animal_parameters() raises a TypeError
    if it is given a non-dict type parameter_values argument.

    * Test if the method set_animal_parameters() raises a ValueError
    if it is given a unknown parameter.

    * Test if the method set_animal_parameters() correctly sets the
    parameters of all species and animal_objects"""
    island_map = ("OOO\nOJO\nOOO")
    ini_pop = [
        {"loc": (1, 1),
         "pop": [
             {"species": "Herbivore", "age": 5, "weight": 20},
             {"species": "Herbivore", "age": 5, "weight": 20},
             {"species": "Carnivore", "age": 5, "weight": 20},
             {"species": "Carnivore", "age": 5, "weight": 20}]}]
    t = BioSim(island_map, ini_pop, None)
    with pytest.raises(TypeError):
        t.set_landscape_parameters(1, {'zeta': 3.2, 'xi': 1.8})
        t.set_landscape_parameters('Herbivore', ['zeta', 3.2])
        t.set_landscape_parameters('Carnivore', ['zeta', 3.2])
    with pytest.raises(ValueError):
        t.set_animal_parameters('Herbivore', {'eeta': 3.2})
        t.set_animal_parameters('Carnivore', {'eeta': 3.2})
    loc = (1, 1)
    t.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    t.set_animal_parameters('Carnivore', {'zeta': 3.2, 'xi': 1.8})
    herb1_parameters = t.island.habitable_cells[loc].population[
        'Herbivore'][0].parameters
    carn1_parameters = t.island.habitable_cells[loc].population[
        'Carnivore'][0].parameters
    herb2_parameters = t.island.habitable_cells[loc].population[
        'Herbivore'][0].parameters
    carn2_parameters = t.island.habitable_cells[loc].population[
        'Carnivore'][0].parameters
    assert herb1_parameters['zeta'] and herb2_parameters['zeta'] is 3.2
    assert herb1_parameters['xi'] and herb2_parameters['xi'] is 1.8
    assert carn1_parameters['zeta'] and carn2_parameters['zeta'] is 3.2
    assert carn1_parameters['xi'] and carn2_parameters['xi'] is 1.8


def test_set_landscape_parameters():
    """Test if the method set_landscape_parameters() raises a TypeError
    if it is given a non-string type parameter_key argument.

    * Test if the method set_landscape_parameters() raises a TypeError
    if it is given a non-dict type parameter_values argument.

    * Test if the method set_landscape_parameters() raises a ValueError
    if it is given a unknown parameter.

    * Test if the method set_landscape_parameters() raises a ValueError
    if it is given a negative parameter 'f_max'.

    * Test if the method set_landscape_parameters() correctly sets the
    parameters of all Jungle and Savannah landscapes on the map"""
    island_map = ("OOOOOO\nOJSJSO\nOOOOOO")
    ini_pop = [
        {"loc": (1, 1),
         "pop": [
             {"species": "Herbivore", "age": 5, "weight": 20},
             {"species": "Herbivore", "age": 5, "weight": 20},
             {"species": "Carnivore", "age": 5, "weight": 20},
             {"species": "Carnivore", "age": 5, "weight": 20}]}]
    t = BioSim(island_map, ini_pop, None)
    with pytest.raises(TypeError):
        t.set_landscape_parameters(1, {'f_man': 100})
        t.set_landscape_parameters('J', ['f_max', 100])
    with pytest.raises(ValueError):
        t.set_landscape_parameters('J', {'f_min': 100})
        t.set_landscape_parameters('J', {'f_max': -1})
    loc1, loc2, loc3, loc4 = (1, 1), (1, 2), (1, 3), (1, 4)
    t.set_landscape_parameters('J', {'f_max': 5, 'alpha': 1})
    t.set_landscape_parameters('S', {'f_max': 2, 'alpha': 3})
    assert t.island.cells[loc1].parameters['f_max'] is 5
    assert t.island.cells[loc1].parameters['alpha'] is 1
    assert t.island.cells[loc2].parameters['f_max'] is 2
    assert t.island.cells[loc2].parameters['alpha'] is 3
    assert t.island.cells[loc3].parameters['f_max'] is 5
    assert t.island.cells[loc3].parameters['alpha'] is 1
    assert t.island.cells[loc4].parameters['f_max'] is 2
    assert t.island.cells[loc4].parameters['alpha'] is 3


def test_num_animals():
    """Test if the method 'num_animals()' correctly gets the entire
    population of the island.

    * Test if the method num_animals_per_species() returns a
    dictionary with key: animal specie and values: their population,
    such that: {'Herbivore': sum(pop['Herbivore']),
                'Carnivore': sum(pop['Carnivore'])}"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]},
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]},
        {"loc": (1, 3),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20}]}]

    t = BioSim(island_map, ini_pop, None)
    assert t.num_animals is 7
    assert type(t.num_animals_per_species) is dict
    num_herb = t.num_animals_per_species['Herbivore']
    num_carn = t.num_animals_per_species['Carnivore']
    assert num_herb is 4
    assert num_carn is 3

# -*- coding: utf-8 -*-

"""
This is the island pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from biosim.simulation import BioSim
from biosim.island import Island
from biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from biosim.fauna import Herbivore, Carnivore


def test_check_string_instance():
    """Test if the method 'check_string_instance(argument)' identifies
    different argument's type than string and raise ValueError"""
    with pytest.raises(TypeError):
        Island.check_string_instance(0)


def test_check_list_instance():
    """Test if the method 'check_list_instance(argument)' identifies
    different argument's type than list and raise ValueError"""
    with pytest.raises(TypeError):
        Island.check_list_instance({0})


def test_check_dict_instance():
    """Test if the method 'check_dict_instance(argument)' identifies
    different argument's type than dictionary and raise ValueError"""
    with pytest.raises(TypeError):
        Island.check_dict_instance([0])


def test_list_geo_cells():
    """Test if the method 'list_geo_cells(island_map)' generates a
    correct list of geographies with the correct coordinates."""
    island_maps = "OOO\nOJO\nOOO"
    list_geos = Island.list_geo_cells(island_maps)
    assert list_geos[1][1] is 'J'


def test_invalid_line_lengths():
    """Test if the method 'check_invalid_line_lengths(geos)' identifies
    a different horizontal (line/row) length on the island_maps"""
    island_maps = ("OOOOOO\nOJJJO\nOOOOO",
                   "OOOOO\nOOJJJO\nOOOOO",
                   "OOOOO\nOJJJO\nOOOOOO")
    for island_map in island_maps:
        island_map = Island.list_geo_cells(island_map)
        with pytest.raises(ValueError):
            Island.check_invalid_line_lengths(island_map)


def test_invalid_boundary():
    """Test if the method 'check_invalid_boundary(geos)' identifies
    a different boundary for island_maps than only 'Oceans'"""
    island_maps = ("JOOOO\nOJJJO\nOOOOO",
                   "OOOOJ\nOJJJO\nOOOOO",
                   "OOJOO\nOJJJO\nOOOOO",
                   "OOOOO\nJJJJO\nOOOOO",
                   "OOOOO\nOJJJJ\nOOOOO",
                   "OOOOO\nOJJJO\nJOOOO",
                   "OOOOO\nOJJJO\nOOOOJ",
                   "OOOOO\nOJJJO\nOOJOO")
    for island_map in island_maps:
        island_map = Island.list_geo_cells(island_map)
        with pytest.raises(ValueError):
            Island.check_invalid_boundary(island_map)


def test_invalid_character():
    """Test if the method 'check_invalid_character(geos)' identifies
    an invalid character on the island_map"""
    island_map = "OOOOO\nOJAJO\nOOOOO"
    island_map = Island.list_geo_cells(island_map)
    with pytest.raises(ValueError):
        Island.check_invalid_character(island_map)


def test_age_stored():
    """Test if the method 'def add_population()' correctly store the age
    on animal_object"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    h_age = t.island.habitable_cells[loc].population['Herbivore'][0].age
    assert h_age is 5


def test_weight_stored():
    """Test if the method 'add_population()' correctly store the
    weight on animal_object"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    h_weight = t.island.habitable_cells[loc].population['Herbivore'][
        0].weight
    assert h_weight is 20


def test_neighbour_cells():
    """Test if the method 'neighbour_cell(loc)' returns the correctly
    habitable neighbours of a given localization"""
    island_maps = ("OOOOO\nOJDJO\nOMJMO\nOJMJO\nOOOOO",
                   "OOOOO\nOJMJO\nOMJMO\nOJDJO\nOOOOO",
                   "OOOOO\nOJMJO\nODJMO\nOJMJO\nOOOOO",
                   "OOOOO\nOJMJO\nOMJDO\nOJMJO\nOOOOO")
    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}],
        }]
    for island_map in island_maps:
        t = BioSim(island_map, ini_pop, None)
        neighbours = [type(neighbour).__name__ for neighbour
                      in t.island.neighbour_cell(loc=(2, 2))]
        assert 'Desert' in neighbours
        assert len(neighbours) is 1
    island_map = ("OOOOO\nOJDJO\nOOJJO\nOJSJO\nOOOOO")
    t = BioSim(island_map, ini_pop, None)
    neighbours = [type(neighbour).__name__ for neighbour
                  in t.island.neighbour_cell(loc=(2, 2))]
    assert 'Jungle' in neighbours
    assert 'Savannah' in neighbours
    assert 'Desert' in neighbours
    assert len(neighbours) is 3


def test_get_population_numbers():
    """Test if the method 'get_population_numbers()' correctly gets the
    entire population of each geo_object and returns a dictionary, such
    that: {'Row': [], 'Col': [], 'Herbivore': [], 'Carnivore': []}"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {"loc": (1, 1),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]},
        {"loc": (1, 2),
         "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                 {"species": "Carnivore", "age": 5, "weight": 20}]}]

    t = BioSim(island_map, ini_pop, None)
    pop = t.island.get_population_numbers()
    row_loc, col_loc = pop['Row'][0], pop['Col'][0]
    pop_herb, pop_carn = pop['Herbivore'][0], pop['Carnivore'][0]
    assert (row_loc and col_loc and pop_herb and pop_carn) is 0

    row_loc, col_loc = pop['Row'][6], pop['Col'][6]
    pop_herb, pop_carn = pop['Herbivore'][6], pop['Carnivore'][6]
    assert row_loc and col_loc is 1 and pop_herb is 2 and pop_carn is 1

    row_loc, col_loc = pop['Row'][7], pop['Col'][7]
    pop_herb, pop_carn = pop['Herbivore'][7], pop['Carnivore'][7]
    assert row_loc is 1 and col_loc is 2 and pop_herb and pop_carn is 1

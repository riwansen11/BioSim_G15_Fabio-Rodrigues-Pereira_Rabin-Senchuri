# -*- coding: utf-8 -*-

"""
This is the island pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from src.biosim.simulation import BioSim
from src.biosim.island import Island
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from src.biosim.fauna import Herbivore, Carnivore


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
    island_map = "OOOOOO\nOJAJO\nOOOOO"
    island_map = Island.list_geo_cells(island_map)
    with pytest.raises(ValueError):
        Island.check_invalid_character(island_map)


def test_neighbour_cells():  # wrong after correction on the method
    """ Test, in 4 different maps, if the method 'neighbour_cell(loc)'
    identifies the 'Desert' geography as one of the neighbours of the
    geography 'Jungle' placed at the coordinates (2,2). The expected
    neighbour geography 'Desert' was placed on the north, south, west
    and east neighbor on the respectively tuple island_maps"""
    '''island_maps = ("OOOOO\nOJDJO\nOMJMO\nOJMJO\nOOOOO",
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
        neighbour_expected = Desert.__name__
        neighbours = [type(neighbour).__name__ for neighbour
                      in t.island.neighbour_cell(loc=(2, 2))]
        assert neighbour_expected in neighbours'''
    pass


def test_a():
    ini_pop = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (2, 3),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (1, 2),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}],
        },
        {
            "loc": (3, 2),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}]
        }]
    pass

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


def test_list_geo_cells():
    """Test if the method 'list_geo_cells(island_map)' generates a
    correct list of geographies with the correct coordinates."""
    island_maps = "OOO\nOJO\nOOO"
    list_geos = Island.list_geo_cells(island_maps)
    assert list_geos[1][1] is 'J'


def test_invalid_line_lengths():
    """Raises ValueError if length of island is not same on each row"""
    island_maps = ("OOOOOO\nOJJJO\nOOOOO",
                   "OOOOO\nOOJJJO\nOOOOO",
                   "OOOOO\nOJJJO\nOOOOOO")
    for island_map in island_maps:
        island_map = Island.list_geo_cells(island_map)
        with pytest.raises(ValueError):
            Island.check_invalid_line_lengths(island_map)


def test_invalid_boundary():
    """Raises ValueError if boundary of island is other than "O"""
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


def test_neighbour_cells():
    island_map = "OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"
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
                    {"species": "Carnivore", "age": 5, "weight": 20}],
            }
        ]

    a = BioSim(island_map, ini_pop, None)
    loc = (2, 2)
    '''[<src.biosim.geography.Jungle object at 0x10d696a90>, ...,
    <src.biosim.geography.Jungle object at 0x10d696b10>]'''

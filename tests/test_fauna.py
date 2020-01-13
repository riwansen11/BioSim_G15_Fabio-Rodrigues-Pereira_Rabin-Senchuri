# -*- coding: utf-8 -*-

import random
import pytest
import math
import numpy as np
# from pytest import approx
from src.biosim.fauna import Fauna

"""
This is the fauna pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"



def test_create_animal():
    h = Herbivore()
    assert h.age == 0
    h.ages()


def test_herbivore_params_keys():
    """
    Tests that the given parameters are in the list of v parameters.
    """
    keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                 'phi_age',
                 'w_half', 'phi_weight', 'mu', 'lambda', 'gamma',
                 'zeta',
                 'xi', 'omega', 'F']
    h = Herbivore()
    assert h.default_params.keys() in keys_list


def test_parameter_type():
    """
    Test parameter are only dictionary
    """
    pytest.raises(TypeError, Animal.set_params, [])


def test_animal_age_weight():
    """
    test if animal age is not int and non-negative
    test if animal age is not int or float and non-negative
    """


def test_default_paraemters():
    """
    test that default parameters has keys as string and values as float
    """
    h = Herbivore()
    for key, value in h.default_params.items():
        assert isinstance(key, str)
        assert isinstance(value, float)


@pytest.mark.parametrize('set_params',
                         [{'w_half': 10.0}, {'phi_weight': 0.1},

                          {'phi_age': 0.2}, {'a_half': 40.0}],

                         indirect=True)
def test_fitness_range(set_params):
    """
    test fitness value is between 0 and 1
    """
    a = Animal
    a.w = np.random.randint(0, 100)
    a.age = np.random.randint(0, 100)
    assert 1 >= a.fitness >= 0


def test_fitness_value(set_params):
    """
    test calculated fitness values with real approx value

    """
    a = Animal
    a.weight = 30
    a.age = 10
    assert a.fitness == approx(0.4102753)

    assert a.fitness == approx(0.25506075)


def test_fitness_update():
    """
    test fitness is updated when weight is changed

    """
    pass


def test_animal_aging():
    """
    test every year animal age updates

    """
    pass


def test_animal_weight_loss():
    """
    Test if animal looses weight

    """
    pass


def test_animal_death():
    """
    test that animal dies when fitness is 0

    """
    pass


def test_no_animal_birth():
    """
    test no birth if number of animal is 1
    """
    pass


def test_animal_eating():
    """
    test animal weight increases after eating
    :return:
    """

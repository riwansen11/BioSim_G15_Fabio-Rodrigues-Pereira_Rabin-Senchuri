# -*- coding: utf-8 -*-

"""
This is the fauna pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from src.biosim.fauna import Population, Herbivore, Carnivore


def test_check_unknown_parameters():
    """Test method 'check_unknown_parameters()' if it does not
    identifies the given parameter and returns ValueError"""
    with pytest.raises(ValueError):
        Herbivore.check_unknown_parameters(params={'zetaa': 100})
        Carnivore.check_unknown_parameters(params={'muu': 100})


def test_check_known_parameters():
    """Test method 'check_unknown_parameters()' if it identifies the
    given parameter and does not return ValueError"""
    Herbivore.check_unknown_parameters(params={'zeta': 100})
    Carnivore.check_unknown_parameters(params={'mu': 100})


def test_create_animal():
    """"""
    '''h = Herbivore()
    assert h.age == 0
    h.ages()'''
    pass


def test_herbivore_params_keys():
    """ Tests that the given parameters are in the list of v
    parameters"""
    '''keys_list = ['w_birth', 'sigma_birth', 'beta', 'eta', 'a_half',
                 'phi_age',
                 'w_half', 'phi_weight', 'mu', 'lambda', 'gamma',
                 'zeta',
                 'xi', 'omega', 'F']
    h = Herbivore()
    assert h.parameters.keys() in keys_list'''
    pass


def test_parameter_type():
    """
    Test parameter are only dictionary
    """
    '''pytest.raises(TypeError, Animal.set_params, [])'''
    pass


def test_animal_age_weight():
    """
    test if animal age is not int and non-negative
    test if animal age is not int or float and non-negative
    """
    pass


def test_default_paraemters():
    """
    test that default parameters has keys as string and values as float
    """
    '''h = Herbivore()
    for key, value in h.parameters.items():
        assert isinstance(key, str)
        assert isinstance(value, float)'''
    pass


'''@pytest.mark.parametrize('set_params',
                         [{'w_half': 10.0}, {'phi_weight': 0.1},
                          {'phi_age': 0.2}, {'a_half': 40.0}],
                         indirect=True)'''


def test_fitness_range():
    """
    test fitness value is between 0 and 1
    """
    '''a = Animal
    a.w = np.random.randint(0, 100)
    a.age = np.random.randint(0, 100)
    assert 1 >= a.fitness >= 0'''
    pass


def test_fitness_value():
    """
    test calculated fitness values with real approx value
    """
    '''a = Animal
    a.weight = 30
    a.age = 10
    assert a.fitness == approx(0.4102753)
    assert a.fitness == approx(0.25506075)'''
    pass


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
    """
    pass

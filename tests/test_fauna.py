# -*- coding: utf-8 -*-

"""
This is the fauna pytest package which is a test package for the 
BioSim packages written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pytest
from src.biosim.simulation import BioSim
from src.biosim.island import Island
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from src.biosim.fauna import Population, Herbivore, Carnivore
import random as rd


@pytest.fixture(autouse=True)
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


def test_animal_got_old():
    """Test if the method 'get_old()' correctly increases in 1 year a
    specie_object age"""
    island_map = "OOOOO\nOJJJO\nOOOOO"
    ini_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20},
                    {"species": "Carnivore", "age": 4, "weight": 20}],
        }]
    t, loc = BioSim(island_map, ini_pop, None), (1, 2)
    herb_object = t.island.habitable_cells[loc].population[
        'Herbivore'][0]
    carn_object = t.island.habitable_cells[loc].population[
        'Carnivore'][0]
    herb_age_1 = herb_object.age
    carn_age_1 = carn_object.age
    herb_object.get_old()
    carn_object.get_old()
    herb_age_2 = herb_object.age
    carn_age_2 = carn_object.age
    assert herb_age_2 is (herb_age_1 + 1)
    assert carn_age_2 is (carn_age_1 + 1)


def test_calculate_fitness_and_formula():
    """Test if the method 'calculate_fitness()' correctly communicates to
    the method 'fit_formula()' and returns the correct fitness of the
    animal (pop_object)'"""
    pass


def test_check__phi_borders():
    """Test if method 'check__phi_borders()' verifies the _phy
    conditions '0 <= _phi <= 1' and returns an ValueError if  not
    satisfied"""
    with pytest.raises(ValueError):
        Herbivore(1, 50).check__phi_borders(-0.9999)
        Carnivore(1, 50).check__phi_borders(-0.9999)
        Herbivore(1, 50).check__phi_borders(1.0001)
        Carnivore(1, 50).check__phi_borders(1.0001)


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
                 'phi_age', 'w_half', 'phi_weight', 'mu', 'lambda',
                 'gamma', 'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax']
    t = Herbivore(1, 50)
    assert t.parameters.keys() in keys_list'''
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


def test_carnivore_kill(mocker):
    """
    test that carnivore kills herbivore if carnivore
    fitness is greater than herbivore fitness and the
    difference between carnivore fitness and herbivore
    fitness divided by DeltaPhiMax parameter is greater
    random value.
    """
    mocker.patch('numpy.random.random', return_value=0.01)
    herbivore = Herbivore()
    carnivore = Carnivore()
    herbivore.fitness, carnivore.fitness = 0.1, 0.8
    assert carnivore.is_herb_killed(herbivore.fitness)


def test_carnivore_eating():
    herbivores = [Herbivore(weight=15, age=5) for _ in range(6)]
    Carnivore.parameters({"DeltaPhiMax": 0.000001})
    carn = Carnivore(weight=500, age=5)
    start_weight = carn.weight
    surviving_herbivores = carn.eating(herbivores)
    new_weight = carn.weight
    assert len(herbivores) > len(surviving_herbivores)
    assert new_weight > start_weight
    assert carn.weight == 537.5

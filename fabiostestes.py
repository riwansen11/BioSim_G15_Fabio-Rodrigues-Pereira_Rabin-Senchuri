from src.biosim.fauna import Population, Herbivore, Carnivore
from src.biosim.simulation import BioSim
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
import pandas as pd
import math as math
import numpy as np

island_map = "OOO\nOJO\nOOO"
ini_herb = [
        {"loc": (1, 1),
         "pop": [
                {"species": "Herbivore", "age": 5, "weight": 40}
                for _ in range(20)
            ]}]

ini_carn = [
        {"loc": (1, 1),
         "pop": [
                {"species": "Carnivore", "age": 5, "weight": 40}
                for _ in range(5)
            ]}]
t = BioSim(island_map, ini_herb, None)
t.add_population(ini_carn)
loc = (1, 1)
t.island.cells[loc].carnivore_feed()

'''herb_0_age = t.island.cells[loc].population['Herbivore'][0].age
herb_0_weight = t.island.cells[loc].population['Herbivore'][0].weight
herb_0_fitness = t.island.cells[loc].population['Herbivore'][0].fitness
print('herb_0_age:', herb_0_age)
print('herb_0_weight:', herb_0_weight)
print('herb_0_fitness:', herb_0_fitness)

herb_1_age = t.island.cells[loc].population['Herbivore'][1].age
herb_1_weight = t.island.cells[loc].population['Herbivore'][1].weight
herb_1_fitness = t.island.cells[loc].population['Herbivore'][1].fitness
print('herb_1_age:', herb_1_age)
print('herb_1_weight:', herb_1_weight)
print('herb_1_fitness:', herb_1_fitness)

carn_0_age = t.island.cells[loc].population['Carnivore'][0].age
carn_0_weight = t.island.cells[loc].population['Carnivore'][0].weight
carn_0_fitness = t.island.cells[loc].population['Carnivore'][0].fitness
print('carn_0_age:', carn_0_age)
print('carn_0_weight:', carn_0_weight)
print('carn_0_fitness:', carn_0_fitness)

carn_1_age = t.island.cells[loc].population['Carnivore'][1].age
carn_1_weight = t.island.cells[loc].population['Carnivore'][1].weight
carn_1_fitness = t.island.cells[loc].population['Carnivore'][1].fitness
print('carn_1_age:', carn_1_age)
print('carn_1_weight:', carn_1_weight)
print('carn_1_fitness:', carn_1_fitness)

t.simulate(1)'''





from src.biosim.fauna import Population, Herbivore, Carnivore
from src.biosim.simulation import BioSim
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
import pandas as pd
import math as math
import numpy as np
import random as rd

island_map = "OOO\nOJO\nOOO"
ini_herb = [
    {"loc": (1, 1),
     "pop": [
         {"species": "Herbivore", "age": rd.randint(1, 10), "weight":
             rd.randint(20, 60)}
         for _ in range(20000)
     ]}]

ini_carn = [
    {"loc": (1, 1),
     "pop": [
         {"species": "Carnivore", "age": rd.randint(1, 10), "weight":
             rd.randint(20, 60)}
         for _ in range(20)
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

t.simulate(1)




global herb_object, h_w, h_f, c_food_desired
        self.population['Carnivore'].sort(key=lambda h: h.fitness,
                                          reverse=True)
        self.population['Herbivore'].sort(key=lambda h: h.fitness)
        for carn_object in self.population["Carnivore"]:
            c_appetite = carn_object.parameters['F']
            c_ate = 0
            c_food_desired = c_appetite - c_ate

            while not c_food_desired <= 0:
                for herb_object in self.population['Herbivore']:
                    h_w = herb_object.weight
                    h_f = herb_object.fitness
                    if carn_object.is_herb_killed(h_f):
                        print('Killed:')
                        print('Food desired', c_food_desired)
                        if h_w <= c_food_desired:
                            print('h_weight <= c_food_desired', h_w, c_food_desired)
                            carn_object.gain_weight(h_w)
                            carn_object.update_fitness()
                            c_food_desired -= h_w
                            print('killed', herb_object)
                            self.population["Herbivore"].remove(herb_object)
                        elif h_w > c_food_desired:
                            print('h_weight > c_food_desired', h_w, c_food_desired)
                            carn_object.gain_weight(c_food_desired)
                            carn_object.update_fitness()
                            c_food_desired -= c_food_desired
                            print('killed', herb_object)
                            self.population["Herbivore"].remove(herb_object)'''


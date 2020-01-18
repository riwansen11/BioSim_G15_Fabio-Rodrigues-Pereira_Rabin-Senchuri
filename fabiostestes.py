from src.biosim.fauna import Population, Herbivore, Carnivore
from src.biosim.simulation import BioSim
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
import pandas as pd
import math as math
import numpy as np

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
carn_age_1 = carn_object
herb_object.get_old()
carn_object.get_old()
herb_age_2 = herb_object.age
carn_age_2 = carn_object
print(herb_age_2 is (herb_age_1 + 1))
print(carn_age_2 is (carn_age_1 + 1))


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
         for _ in range(20)
     ]}]

ini_carn = [
    {"loc": (1, 1),
     "pop": [
         {"species": "Carnivore", "age": rd.randint(1, 10), "weight":
             rd.randint(20, 60)}
         for _ in range(200)
     ]}]
t = BioSim(island_map, ini_herb, None)
t.add_population(ini_carn)
loc = (1, 1)
t.island.cells[loc].carnivore_feed()
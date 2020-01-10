# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import time
import random
from src.biosim.animals import Animal, Herbivore, Carnivores
from src.biosim.pop_gen import Population
from src.biosim.simulation import BioSim
from src.biosim.landscape import Map, Tile, Ocean, Desert, Mountain, \
    Jungle, Savannah

if __name__ == '__main__':
    c = Map()
    cood = c.geolist()
    herb = Herbivore()
    carn = Carnivores()

    # p is an object of the called Population class
    p = Population(random.randint(1, 20),  # random number of herb
                   herb.coordinations(),  # random coordination of herb
                   random.randint(1, 10),  # random number of carn
                   carn.coordinations()  # random coordination of carn
                   )

    # method of Population.get_animals() called
    list_herb = p.get_animals()

    sim = BioSim(island_map=c.geolist(), ini_pop=list_herb, seed=123456)

    # Animal.Herbivore.set_animal_params("Herbivore", {"zeta": 3.2,
    #                                                 "xi": 1.8})
    # sim.set_animal_parameters(
    #     "Carnivore",
    #     {
    #         "a_half": 70,
    #         "phi_age": 0.5,
    #         "omega": 0.3,
    #         "F": 65,
    #         "DeltaPhiMax": 9.0,
    #     },
    # )
    Jungle.set_landscape_parameters({"f_max": 700})
    sim.add_herb()
    sim.simulate(20, vis_years=1, img_years=2000)

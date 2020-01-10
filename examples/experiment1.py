# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt
import numpy as np

import time

from src.biosim.animals import Animal
from src.biosim.pop_gen import Population
from src.biosim.simulation import BioSim
import random

from src.biosim.landscape import Ocean
from src.biosim.landscape import Desert
from src.biosim.landscape import Mountain
from src.biosim.landscape import Jungle
from src.biosim.landscape import Savannah

if __name__ == '__main__':
    # plt.ion()
    #
    geogr = """\
                   OOOOOOOOOOOOOOOOOOOOO
                   OOOOOOOOSMMMMJJJJJJJO
                   OSSSSSJJJJMMJJJJJJJOO
                   OSSSSSSSSSMMJJJJJJOOO
                   OSSSSSJJJJJJJJJJJJOOO
                   OSSSSSJJJDDJJJSJJJOOO
                   OSSJJJJJDDDJJJSSSSOOO
                   OOSSSSJJJDDJJJSOOOOOO
                   OSSSJJJJJDDJJJJJJJOOO
                   OSSSSJJJJDDJJJJOOOOOO
                   OOSSSSJJJJJJJJOOOOOOO
                   OOOSSSSJJJJJJJOOOOOOO
                   OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)  # spaces deleted
    # creates a list of strings with a line for each element
    gl = geogr.splitlines()
    geolist = []  # creates a empty list
    for g in gl:  # append a list with each line of geogr
        geolist.append(list(g))
    for rownum, row in enumerate(geolist):
        for colnum, itemvalue in enumerate(row):
            if geolist[rownum][colnum] == 'O':
                geolist[rownum][colnum] = Ocean((rownum, colnum))
            elif geolist[rownum][colnum] == 'M':
                geolist[rownum][colnum] = Mountain((rownum, colnum))
            elif geolist[rownum][colnum] == 'D':
                geolist[rownum][colnum] = Desert((rownum, colnum))
            elif geolist[rownum][colnum] == 'J':
                geolist[rownum][colnum] = Jungle((rownum, colnum))
            else:
                geolist[rownum][colnum] = Savannah((rownum, colnum))

    herb_cord = []
    carn_cord = []

    # 2500 random locations of herb with the place restrictions
    # needs to think about seeding
    # Use herb_place_restriction to not have coordination where is not
    # allowed
    for i in range(50):
        for j in range(50):
<<<<<<< HEAD
            herb_cord.append((random.randint(1,13), random.randint(1,
                                                                  21)))

    for i in range(50):
        for j in range(50):
            carn_cord.append((random.randint(1,13), random.randint(1,
                                                                  21)))
    print(herb_cord)
    p = Population(random.randint(1, 20), herb_cord, random.randint(1, 10), carn_cord)
=======
            herb_cord.append((random.randint(1, 13),
                              random.randint(1, 21))
                             )
    # 2500 random locations of carn with the place restrictions
    # needs to think about seeding
    # Use carn_place_restriction to not have coordination where is not
    # allowed
    for i in range(50):
        for j in range(50):
            carn_cord.append((random.randint(1, 13),
                              random.randint(1, 21))
                             )

    # p is an object of the called Population class
    p = Population(random.randint(1, 20),  # random number of herb
                   herb_cord,  # all random coordination of herb
                   random.randint(1, 10),  # random number of carn
                   carn_cord  # all random coordination of carn
                   )

    # method of Population.get_animals() called
>>>>>>> rabin
    list_herb = p.get_animals()

    sim = BioSim(island_map=geolist, ini_pop=list_herb,
                 seed=123456)

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



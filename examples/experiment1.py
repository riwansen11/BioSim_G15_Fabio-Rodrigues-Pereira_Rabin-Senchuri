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
    geogr = textwrap.dedent(geogr)
    gl = geogr.splitlines()
    geolist = []
    for g in gl:
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
    for i in range(50):
        for j in range(50):
            herb_cord.append((random.randint(1,22), random.randint(1,21)))

    for i in range(50):
        for j in range(50):
            carn_cord.append((random.randint(1,22), random.randint(1,21)))
    print(herb_cord)
    p = Population(random.randint(1, 20), herb_cord, random.randint(1, 10), carn_cord)
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



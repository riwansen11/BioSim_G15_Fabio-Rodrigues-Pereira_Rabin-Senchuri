# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt
import numpy as np

import time
from src.biosim.pop_gen import Population
from src.biosim.simulation import Simulation
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

    sim = Simulation(island_map=geolist, ini_pop=list_herb,
                 seed=123456)

    # sim.set_animal_parameters('Herbivore', {'zeta': 3.2, 'xi': 1.8})
    #
    # sim.set_animal_parameters('Carnivore', {'a_half': 70, 'phi_age': 0.5,
    #                                         'omega': 0.3, 'F': 65,
    #                                         'DeltaPhiMax': 9.0})
    # sim.set_landscape_parameters('J', {'f_max': 700})
    sim.add_herb()
    sim.simulate(20, vis_years=1, img_years=2000)

#    sim.add_population(list_carn)
    #sim.simulate(50, vis_years=1, img_years=2000)

    rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                 'M': (0.5, 0.5, 0.5),  # grey
                 'J': (0.0, 0.6, 0.0),  # dark green
                 'S': (0.5, 1.0, 0.5),  # light green
                 'D': (1.0, 1.0, 0.5)}  # light yellow
    landscape_rgb = [[rgb_value[column] for column in row]
                for row in gl]

    fig = plt.figure()

    axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
    axim.imshow(landscape_rgb)
    axim.set_xticks(range(len(landscape_rgb[0])))
    axim.set_xticklabels(range(1, 1 + len(landscape_rgb[0])))
    axim.set_yticks(range(len(landscape_rgb)))
    axim.set_yticklabels(range(1, 1 + len(landscape_rgb)))

    axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
    axlg.axis('off')
    for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                               'Savannah', 'Desert')):
        axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                     edgecolor='none',
                                     facecolor=rgb_value[name[0]]))
        axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    plt.show()



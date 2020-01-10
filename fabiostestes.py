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
print(geogr)

geogr = textwrap.dedent(geogr)
gl = geogr.splitlines()
geolist = []  # creates a empty list

for g in gl:  # append a list with each line of geogr
    geolist.append(list(g))

print(geogr)
print(gl)
print(geolist)
print(enumerate(geolist))

for rownum, row in enumerate(geolist):
    print(rownum)
    print(row)
    for colnum, itemvalue in enumerate(row):
        print(colnum)
        print(itemvalue)
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

print(geolist)
print(type(geolist[0][0]))

herb_cord = []
carn_cord = []

for i in range(5):
    for j in range(5):
        herb_cord.append((random.randint(1, 22), random.randint(1, 21)))

print(herb_cord)
print(len(herb_cord))

for i in range(5):
    for j in range(5):
        carn_cord.append((random.randint(1, 13),
                          random.randint(1, 21))
                         )

print(carn_cord)
print(len(carn_cord))

# p is an object of the called Population class
p = Population(random.randint(1, 20),  # random number of herb
               herb_cord,  # all random coordination of herb
               random.randint(1, 10),  # random number of carn
               carn_cord  # all random coordination of carn
               )

list_herb = p.get_animals()

print(list_herb)


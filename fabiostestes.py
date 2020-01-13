from src.biosim.simulation import BioSim
import numpy as np

loc = (10, 10)
a = BioSim(None, None, None)
print(a.geography.cells)
print(loc)
print(a.geography.cells[loc[0]][loc[1]])

if a.geography.cells[loc[0]][loc[1]] in ('J', 'S', 'D'):
    print('True')

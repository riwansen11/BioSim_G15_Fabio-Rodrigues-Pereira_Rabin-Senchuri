# -*- coding: utf-8 -*-

import numpy as np
import random

"""
This is the animals model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Animals:
    params_examples = {'Herbivore': (8.0, 1.5, 0.9, 0.05, 40.0, 0.2,
                                     10.0, 0.1, 0.25, 1.0, 0.2, 3.5,
                                     1.2, 0.4, 10.0, None),
                       'Carnivore': (6.0, 1.0, 0.75, 0.125, 60.0, 0.4,
                                     4.0, 0.4, 0.4, 1.0, 0.8, 3.5, 1.1,
                                     0.9, 50.0, 10.0)
                       }

    def __init__(self):
        pass

    def k_parameters(self):
        k_parameters = ('w_birth', 'sigma_birth', 'beta', 'eta',
                        'a_half', 'phi_age', 'w_half', 'phi_weight',
                        'mu', 'lambda', 'gamma', 'zeta', 'xi',
                        'omega', 'F', 'DeltaPhiMax')


class Herbivore(Animals):
    pass


class Carnivores(Animals):
    pass

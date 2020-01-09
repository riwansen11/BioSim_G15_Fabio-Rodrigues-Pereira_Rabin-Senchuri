# # -*- coding: utf-8 -*-
#
# """
# """
#
# __author__ = ""
# __email__ = ""
#
#
# class BioSim:
#     def __init__(
#         self,
#         island_map,
#         ini_pop,
#         seed,
#         ymax_animals=None,
#         cmax_animals=None,
#         img_base=None,
#         img_fmt="png",
#     ):
#         """
#         :param island_map: Multi-line string specifying island geography
#         :param ini_pop: List of dictionaries specifying initial population
#         :param seed: Integer used as random number seed
#         :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
#         :param cmax_animals: Dict specifying color-code limits for animal densities
#         :param img_base: String with beginning of file name for figures, including path
#         :param img_fmt: String with file type for figures, e.g. 'png'
#
#         If ymax_animals is None, the y-axis limit should be adjusted automatically.
#
#         If cmax_animals is None, sensible, fixed default values should be used.
#         cmax_animals is a dict mapping species names to numbers, e.g.,
#            {'Herbivore': 50, 'Carnivore': 20}
#
#         If img_base is None, no figures are written to file.
#         Filenames are formed as
#
#             '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
#
#         where img_no are consecutive image numbers starting from 0.
#         img_base should contain a path and beginning of a file name.
#         """
#
#     def set_animal_parameters(self, species, params):
#         """
#         Set parameters for animal species.
#
#         :param species: String, name of animal species
#         :param params: Dict with valid parameter specification for species
#         """
#
#         if species == "Herbivore":
#             params = {
#                 'w_birth': 8.0,
#                 'sigma_birth': 1.5,
#                 'beta': 0.9,
#                 'eta': 0.05,
#                 'a_half': 40.,
#                 'phi_age': 0.2,
#                 'w_half': 10.,
#                 'phi_weight': 0.1,
#                 'mu': 0.25,
#                 'lambda': 1,
#                 'gamma': 0.2,
#                 'zeta': 3.5,
#                 'xi': 1.2,
#                 'omega': 0.4,
#                 'F': 10.0
#             }
#         else:
#             params = {
#                 'w_birth': 6.0,
#                 'sigma_birth': 1.0,
#                 'beta': 0.75,
#                 'eta': 0.125,
#                 'a_half': 60.,
#                 'phi_age': 0.4,
#                 'w_half': 4.0,
#                 'phi_weight': 0.4,
#                 'mu': 0.4,
#                 'lambda': 1,
#                 'gamma': 0.8,
#                 'zeta': 3.5,
#                 'xi': 1.1,
#                 'omega': 0.9,
#                 'F': 50.0,
#                 'DeltaPhiMax': 10.0
#             }
#
#     def set_landscape_parameters(self, landscape, params):
#         """
#         Set parameters for landscape type.
#
#         :param landscape: String, code letter for landscape
#         :param params: Dict with valid parameter specification for landscape
#         """
#         if landscape == "J":
#             params = {
#                 "f_max": 800
#             }
#         elif landscape == "S":
#             params = {
#                 "f_max": 300,
#                 "alpha": 0.3
#             }
#
#     def simulate(self, num_years, vis_years=1, img_years=None):
#         """
#         Run simulation while visualizing the result.
#
#         :param num_years: number of years to simulate
#         :param vis_years: years between visualization updates
#         :param img_years: years between visualizations saved to files (default: vis_years)
#
#         Image files will be numbered consecutively.
#         """
#
#     def add_population(self, population):
#         """
#         Add a population to the island
#
#         :param population: List of dictionaries specifying population
#         """
#
#     @property
#     def year(self):
#         """Last year simulated."""
#
#     @property
#     def num_animals(self):
#         """Total number of animals on island."""
#
#     @property
#     def num_animals_per_species(self):
#         """Number of animals per species in island, as dictionary."""
#
#     @property
#     def animal_distribution(self):
#         """Pandas DataFrame with animal count per species for each cell on island."""
#
#     def make_movie(self):
#         """Create MPEG4 movie from visualization images saved."""

from src.biosim.animals import Animal
from src.biosim.animals import Herbivore
from src.biosim.landscape import Jungle
from src.biosim.landscape import Ocean
from src.biosim.landscape import Savannah
from src.biosim.landscape import Desert
from src.biosim.landscape import Mountain
import random
import numpy as np
import time
import matplotlib.pyplot as plt
from src.biosim.landscape import Tile


class BioSim:
    """
     Run simulation while visualizing the result.
    """

    def __init__(self, island_map, ini_pop, seed):

        """
        Parameters
        ----------
            island_map: string
                Multi-line string specifying island geography
            ini_pop: list
                list of dictionaries specifying initial population
            seed: int
                Integer used as random number seed

        Returns
        -------....
            int
                simulate cells

        """
        self.island_map = island_map
        self.list_herb = ini_pop
        random.seed(seed)
        self._final_year = None
        self._year = 0

        self.cell = [(island_map[rownum][colnum]) for rownum, row in enumerate(island_map) for
                     colnum, itemvalue in enumerate(row)]


    def set_animal_parameters(self, species, params):

        """
            Set parameters for animal species.

            :param species: String, name of animal species
            :param params: Dict with valid parameter specification for species
        """

        if species == "Herbivore":
            a = Animal()



    def set_landscape_parameters(self, landscape, params):
        """
            Set parameters for landscape type.

            :param landscape: String, code letter for landscape
            :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "J":
            params = {
                "f_max": 800
            }
        elif landscape == "S":
            params = {
                "f_max": 300,
                "alpha": 0.3
            }
    def add_herb(self):
        """
        Returns
        -------
            list
                List of Herbivores
        """
        for c in self.cell:
            if not c.habitable:
                continue
            c.add_herb(self.list_herb)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
         Run simulation while visualizing the result.

         Parameters
         ----------
            num_years: int
                number of years to simulate
            vis_years: int
                years between visualization updates
            img_years: int
                years between visualizations saved to files (default: vis_years)

        """
        for c in self.cell:
            #print(c)
            if not c.habitable:
                continue
            # c.add_herb(self.list_herb)
            for year in range(num_years):
                c.grow()
                c.h_feed()
                #c.c_feed()
                c.birth()
                #c.migration()
                c.aging()
                c.loose_weight()
                c.death()
                print(year, c.num_herbs())


    def add_population(self, list_carn):
        """
           Parameters
           ----------
               list_carn: list
                   list of carnivores

           Returns
           -------
               list
                   new list of carnivores

           """
        for c in self.cell:
            if not c.habitable:
                continue
            c.add_carn(list_carn)



# -*- coding: utf-8 -*-

"""
This is the simulation model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import pandas as pd
import random as rd
from src.biosim.island import Island


class BioSim:
    example_geogr = """\
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

    def __init__(self, island_map, ini_pop, seed, ymax_animals=None,
                 cmax_animals=None, img_base=None, img_fmt='png'):
        """
        :param island_map: Multi-line string specifying island geography.
        :param ini_pop: List of dictionaries specifying initial
        population.
        :param seed: Integer used as random number seed.
        :param ymax_animals: Number specifying y-axis limit for graph
        showing animal numbers.
        :param cmax_animals: Dict specifying color-code limits for
        animal densities.
        :param img_base: String with beginning of file name for figures,
        including path.
        :param img_fmt: String with file type for figures, e.g. ’png’.

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should
        be used. cmax_animals is a dict mapping species names to numbers,
        e.g., {’Herbivore’: 50, ’Carnivore’: 20}.

        If img_base is None, no figures are written to file. Filenames
        are formed as ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.

        img_base should contain a path and beginning of a file name.
        """
        island_map = self.example_geogr if island_map is None \
            else island_map

        self.island = Island(island_map)
        self.island.add_population(ini_pop)
        self.seed = rd.seed(seed)
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt

    def set_animal_parameters(self, species, params):
        """
            Set parameters for animal species.

            :param species: String, name of animal species.
            :param params: Dict with valid parameter specification for
            species.
        """
        self.island.set_parameters(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
            Set parameters for landscape type.

            :param landscape: String, code letter for landscape.
            :param params: Dict with valid parameter specification for
            landscape.
        """
        self.island.set_parameters(landscape, params)

    def add_population(self, population):
        """

        :param population: List of dictionaries specifying population:
        """
        self.island.add_population(population)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: int number of years to simulate.
        :param vis_years: int years between visualization updates.
        :param img_years: int years between visualizations saved to files
        (default: vis_years).

        Image files will be numbered consecutively.
        """
        self.island.yearly_cycle()

    @property
    def year(self):
        """Last year simulated"""
        pass

    @property
    def num_animals(self):  # tested
        """Total number of animals on island"""
        pop = self.island.get_population_numbers()
        return sum(pop['Herbivore']) + sum(pop['Carnivore'])

    @property
    def num_animals_per_species(self):  # tested
        """Number of animals per species in island, as dictionary"""
        pop = self.island.get_population_numbers()
        return {'Herbivore': sum(pop['Herbivore']),
                'Carnivore': sum(pop['Carnivore'])}

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island"""
        pop = self.island.get_population_numbers()
        return pd.DataFrame(pop)

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
        pass

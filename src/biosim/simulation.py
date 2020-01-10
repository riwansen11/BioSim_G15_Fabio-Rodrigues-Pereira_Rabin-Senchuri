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
            #print(len(c))
            if not c.habitable:
                continue
            # c.add_herb(self.list_herb)
            for year in range(num_years):
                c.grow()
                c.h_feed()

                c.birth()

                c.aging()
                c.loose_weight()
                c.death()
                print(year, c.num_herbs())






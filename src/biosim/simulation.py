# -*- coding: utf-8 -*-

"""
This is the Simulation model which functions with the BioSim package
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


import pandas as pd
import random as rd
from src.biosim.island import Island
import os
import numpy as np
import matplotlib

'''matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import subprocess

# Update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'convert'

# Update this to the directory and file-name beginning for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('data')

_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_MOVIE_FORMAT = 'mp4'''


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

    def __init__(self, island_map, ini_pop, seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_dir=_DEFAULT_GRAPHICS_DIR,
                 img_name=_DEFAULT_GRAPHICS_NAME,
                 img_fmt='png'):
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

        '''self.color_by_square_type = {'O': mcolors.to_rgb('aqua'),
                                     'M': mcolors.to_rgb('darkgray'),
                                     'J': mcolors.to_rgb('forestgreen'),
                                     'S': mcolors.to_rgb('yellowgreen'),
                                     'D': mcolors.to_rgb('khaki')}

        self.island_map_colors = [[self.color_by_square_type[column] for
                                   column in row] for row in
                                  island_map.splitlines()]
        
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self.img_fmt = img_fmt

        self.step = 0
        self.final_step = None
        self.fig = None
        self.island_map = None
        self.img_axis = None
        self.mean_ax = None
        self.herbivore_line = None
        self.carnivore_line = None
        self.herb_dist = None
        self.carn_dist = None
        self.herb_img_axis = None
        self.carn_img_axis = None

        if img_dir is not None:
            self.img_base = os.path.join(img_dir, img_name)
        else:
            self.img_base = None

        self.img_ctr = 0
        self.img_fmt = img_fmt'''

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
        '''if img_years is None:
            img_years = vis_years
        self.final_step = self.step + num_years
        self.setup_graphics()
        while self.step < self.final_step:
            total_animal = self.num_animals()
            if self.num_animals() == 0:
                break

            if self.step % vis_years == 0:
                self.update_graphics()

            if self.step % img_years == 0:
                self.save_graphics()

            self.island.yearly_cycle()
            self.step += 1'''
        self.island.yearly_cycle()

    @property
    def num_animals(self):  # tested
        """Total number of animals on island"""
        pop = self.island.get_population_numbers()
        return sum(pop['Herbivore']) + sum(pop['Carnivore'])

    @property
    def year(self):
        """Last year simulated"""
        pass

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

    '''def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup_graphics(self):  # used on simulation
        if self.fig is None:
            self.fig = plt.figure()
            self.fig.canvas.set_window_title('BioSim Interactive Window')
            mng = plt.get_current_fig_manager()
            mng.window.resizable(False, False)

        if self.island_map is None:
            self.make_static_map()

        if self.mean_ax is None:
            self.mean_ax = self.fig.add_subplot(2, 2, 2)
            self.mean_ax.set_ylim(0, 16000)

        self.mean_ax.set_xlim(0, self.final_step + 1)
        self.make_herbivore_line()
        self.make_carnivore_line()

        if self.herb_dist is None:
            self.herb_dist = self.fig.add_subplot(2, 2, 3)
            self.herb_img_axis = None

        if self.carn_dist is None:
            self.carn_dist = self.fig.add_subplot(2, 2, 4)
            self.carn_img_axis = None

        self.fig.tight_layout()

    def make_herbivore_line(self):  # used on setup_graphics
        """
        Creates the Herbivore interactive plot, i.e. the graph in the
        interactive graphics window showing the total number of herbivores on
        the island.

        """
        if self.herbivore_line is None:
            herbivore_plot = self.mean_ax.plot(np.arange(0, self.final_step),
                                               np.nan * np.ones(self.final_step))
            self.herbivore_line = herbivore_plot[0]
        else:
            xdata, ydata = self.herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_step)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self.herbivore_line.set_data(np.hstack((xdata, xnew)),
                                             np.hstack((ydata, ynew)))

    def make_carnivore_line(self):  # used on setup_graphics
        """
        Creates the Carnivore interactive plot, i.e. the graph in the
        interactive graphics window showing the total number of Carnivores on
        the island.

        """
        if self.carnivore_line is None:
            carnivore_plot = self.mean_ax.plot(np.arange(0, self.final_step),
                                               np.nan * np.ones(self.final_step))
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_step)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self.carnivore_line.set_data(np.hstack((xdata, xnew)),
                                             np.hstack((ydata, ynew)))

    def make_static_map(self):  # setup_graphics
        """
        Creates a static map, i.e. a plot of the island's geography with a
        color code for each of the island landscape types.

        Notes
        -----
        This map does not change during the simulation, and does not display
        Herbivore or Carnivore activity.

        """
        self.island_map = self.fig.add_subplot(2, 2, 1)
        self.island_map.imshow(self.island_map_colors,interpolation='nearest')

        self.island_map.set_xticks(range(0, len(self.island_map_colors[0]), 5))
        self.island_map.set_xticklabels(range(1, 1 + len(self.island_map_colors[0]), 5))

        self.island_map.set_yticks(range(0, len(self.island_map_colors), 5))
        self.island_map.set_yticklabels(range(1, 1 + len(self.island_map_colors), 5))

    def update_count_graph(self, island_animal_count):  # used on update_graphics
        """
        Updates the graphics in the upper-right corner of the graphics window
        in which the the total Herbivore and Carnivore population sizes are
        displayed.

        Parameters
        ----------
        island_animal_count : dict
            Dictionary with keys 'herbivores' and 'carnivores' for which the
            values are the total number of herbivores and carnivores,
            respectively.

        """
        herb_count, carn_count = list(island_animal_count.values())
        herb_ydata = self.herbivore_line.get_ydata()
        herb_ydata[self.step] = herb_count
        self.herbivore_line.set_ydata(herb_ydata)

        carn_ydata = self._carnivore_line.get_ydata()
        carn_ydata[self.step] = carn_count
        self._carnivore_line.set_ydata(carn_ydata)

    def update_herb_dist(self, herb_dist):  # used on update_graphics
        """
        Updates the graphics in the lower-left corner of the graphics window
        in which Herbivore distribution per square is represented as a
        two-dimensional heat map.

        Parameters
        ----------
        herb_dist : numpy.ndarray

        """
        if self.herb_img_axis is not None:
            self.herb_img_axis.set_data(herb_dist)
        else:
            self.herb_img_axis = self.herb_dist.imshow(herb_dist, 
                                                       vmin=0,
                                                       vmax=200,
                                                       interpolation='nearest',
                                                       aspect='auto')

            self.herb_dist.set_xticks(range(0, len(self.island_map_colors[0]), 5))
            self.herb_dist.set_xticklabels(range(1, 1 + len(self.island_map_colors[0]), 5))

            self.herb_dist.set_yticks(range(0, len(self.island_map_colors), 5))
            self.herb_dist.set_yticklabels(range(1, 1 + len(self.island_map_colors), 5))
            self.herb_dist.set_title('Herbivore distribution')

    def update_carn_dist(self, carn_dist):  # used on update_graphics
        """
        Updates the graphics in the lower-right corner of the graphics window
        in which Carnivore distribution per square is represented as a
        two-dimensional heat map.

        Parameters
        ----------
        carn_dist : numpy.ndarray

        """
        if self.carn_img_axis is not None:
            self.carn_img_axis.set_data(carn_dist)
        else:
            self._carn_img_axis = self.carn_dist.imshow(carn_dist, 
                                                        vmin=0,
                                                        vmax=200,
                                                        interpolation='nearest',
                                                        aspect='auto')

            self.carn_dist.set_xticks(range(0, len(self.island_map_colors[0]), 5))
            self.carn_dist.set_xticklabels(range(1, 1 + len(self.island_map_colors[0]), 5))

            self.carn_dist.set_yticks(range(0, len(self.island_map_colors), 5))
            self.carn_dist.set_yticklabels(range(1, 1 + len(self.island_map_colors), 5))
            self.carn_dist.set_title('Carnivore distribution')

    def update_graphics(self):  # used on simulate
        """
        Updates the interactive graphics window with real-time data and
        includes current year of simulation in upper-left corner.

        """
        animal_count = self.animal_distribution
        row, col = len(self.island_map_colors), \
                   len(self.island_map_colors[0])

        self.update_count_graph(self.num_animals_per_species)
        self.update_herb_dist(np.array(animal_count.herbivores).reshape(row, col))
        self.update_carn_dist(np.array(animal_count.carnivores).reshape(row, col))

        plt.pause(1e-6)

        self.fig.suptitle('Year: {}'.format(self.step + 1), x=0.105)

    def save_graphics(self):  # used on simulate
        """
        Saves graphics to file if file name is given.

        """
        if self.img_base is None:
            return plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                                num=self.img_ctr,
                                                                type=self.img_fmt))
        self.img_ctr += 1'''

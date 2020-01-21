# -*- coding: utf-8 -*-

"""
This is the Simulation model which functions with the BioSim package
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import os
import subprocess
import textwrap
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from .island import Island

matplotlib.use('macosx')

# update these variables to point to your ffmpeg and convert binaries
FFMPEG_BINARY = 'ffmpeg'
CONVERT_BINARY = 'magick'

DEFAULT_IMAGE_BASE = os.path.join('..', 'BioSim')
DEFAULT_IMAGE_FORMAT = 'png'
DEFAULT_MOVIE_FORMAT = 'gif'


class BioSim:
    """Responsible to provide to the user an interface for simulation as
    well as visualization."""

    map_colors = {
        "O": mcolors.to_rgba("navy"),
        "J": mcolors.to_rgba("forestgreen"),
        "S": mcolors.to_rgba("#e1ab62"),
        "D": mcolors.to_rgba("salmon"),
        "M": mcolors.to_rgba("lightslategrey"),
    }
    map_labels = {
        "O": "Ocean",
        "J": "Jungle",
        "S": "Savannah",
        "D": "Desert",
        "M": "Mountain",
    }

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=DEFAULT_IMAGE_BASE,
                 img_fmt=DEFAULT_IMAGE_FORMAT):
        """
        BioSims package constructor.

        Parameters
        ----------
        island_map:
            Multi-line string specifying island geography.

        ini_pop:
            List of dictionaries specifying initial population.

        seed:
            Integer used as random number seed.

        ymax_animals:
            Number specifying y-axis limit for graph showing animal
            numbers.

        cmax_animals:
            Dict specifying color-code limits for animal densities.

        img_base:
            String with beginning of file name for figures, including
            path.

        img_fmt:
            String with file type for figures, e.g. ’png’.


        * If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        * If cmax_animals is None, sensible, fixed default values should
        be used. cmax_animals is a dict mapping species names to numbers,
        e.g., {’Herbivore’: 50, ’Carnivore’: 20}.

        * If img_base is None, no figures are written to file. Filenames
        are formed as ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.

        * img_base should contain a path and beginning of a file name.
        """
        self._map = island_map
        self.island = Island(self._map)
        self.island.add_population(ini_pop)
        np.random.seed(seed)
        self.last_year = 0
        self.year_num = 0
        self.final_year = None
        self.img_base = img_base
        self.img_nums = 0
        self.img_fmt = img_fmt

        self.fig = None
        self._island_map = None
        self._img_axis = None
        self._mean_ax = None
        self._herbivore_line = None
        self._carnivore_line = None
        self._herb_dist = None
        self._carn_dist = None
        self._herb_img_axis = None
        self._carn_img_axis = None

    @property
    def generate_map_array(self):
        """

        Returns
        ----------


        """
        lines = textwrap.dedent(self._map).splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells != len(line):
                raise ValueError(
                    'All lines in the map must have the same number of '
                    'cells.')
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError(
                        f"'{letter}' is not a valid landscape type. "
                        f"Must be one of {set(self.map_colors.keys())}"
                    )
                map_array[-1].append(self.map_colors[letter])

        return map_array

    @property
    def num_animals(self):
        """Total number of animals on island

        Returns
        ----------
            Int with the total number of population in the Island.
        """
        pop = self.island.get_population_numbers()
        return sum(pop['Herbivore']) + sum(pop['Carnivore'])

    @property
    def year(self):
        """Last year simulated.

        Returns
        ----------
            int
        """
        return self.last_year

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary

        Returns
        ----------
            -> Dictionary with the species as keys and number of each
               population as values.
        """
        pop = self.island.get_population_numbers()
        return {'Herbivore': sum(pop['Herbivore']),
                'Carnivore': sum(pop['Carnivore'])}

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island.

        Returns
        ----------
            Pandas DataFrame with the simulated data.
        """
        data = self.island.get_population_numbers()
        return pd.DataFrame(data, columns=['Row',
                                           'Carnivore',
                                           'Col',
                                           'Herbivore'])

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species: str
            String, name of animal species.

        params: dict
            Dict with valid parameter specification for species.
        """
        self.island.set_parameters(species, params)

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape: str
            String, code letter for landscape.

        params: dict
            Dict with valid parameter specification for landscape.
        """
        self.island.set_parameters(landscape, params)

    def add_population(self, population):
        """
        Add population to the island cells.

        Parameters
        ----------
        population: list of dicts
            List of dictionaries specifying population:
        """
        self.island.add_population(population)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """

        Parameters
        ----------
        num_years: int

        vis_years: int

        img_years: int

        """
        if img_years is None:
            img_years = vis_years

        self.last_year += num_years
        self.final_year = self.year_num + num_years
        self.setup_graphics()

        while self.year_num < self.final_year:

            if self.num_animals is 0:
                break

            if self.year_num % vis_years is 0:
                self.update_graphics()

            if self.year_num % img_years is 0:
                self.save_graphics()

            self.island.yearly_cycle()
            self.year_num += 1

    def make_movie(self, mov_fmt=DEFAULT_MOVIE_FORMAT):
        """
        This method returns makes the movie in gif format.

        Parameters
        ----------
        mov_fmt: 'gif'
            DEFAULT_MOVIE_FORMAT = 'gif'
        """
        try:
            subprocess.check_call([CONVERT_BINARY,
                                   '-delay', '1',
                                   '-loop', '0',
                                   '{}_*.png'.format(self.img_base),
                                   '{}.{}'.format(self.img_base,
                                                  mov_fmt)])

        except subprocess.CalledProcessError as err:
            raise RuntimeError('Convert failed with: {}'.format(err))

    def setup_graphics(self):
        if self.fig is None:
            self.fig = plt.figure(figsize=[12, 7])
            self.fig.canvas.set_window_title('BioSim Window')
            # mng = plt.get_current_fig_manager()
            # mng.window.resizable(False, False)

        if self._island_map is None:
            self._make_static_map()

        if self._mean_ax is None:
            self._mean_ax = self.fig.add_subplot(2, 2, 2)
            self._mean_ax.set_ylim(0, 20000)

        self._mean_ax.set_xlim(0, self.final_year + 1)
        self._make_herbivore_line()
        self._make_carnivore_line()

        if self._herb_dist is None:
            self._herb_dist = self.fig.add_subplot(2, 2, 3)
            self._herb_img_axis = None

        if self._carn_dist is None:
            self._carn_dist = self.fig.add_subplot(2, 2, 4)
            self._carn_img_axis = None

        self.fig.tight_layout()

    def _make_herbivore_line(self):
        if self._herbivore_line is None:
            herbivore_plot = self._mean_ax.plot(
                np.arange(0, self.final_year),
                np.nan * np.ones(
                    self.final_year))
            self._herbivore_line = herbivore_plot[0]
        else:
            xdata, ydata = self._herbivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._herbivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def _make_carnivore_line(self):
        if self._carnivore_line is None:
            carnivore_plot = self._mean_ax.plot(
                np.arange(0, self.final_year),
                np.nan * np.ones(
                    self.final_year))
            self._carnivore_line = carnivore_plot[0]
        else:
            xdata, ydata = self._carnivore_line.get_data()
            xnew = np.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self._carnivore_line.set_data(np.hstack((xdata, xnew)),
                                              np.hstack((ydata, ynew)))

    def _make_static_map(self):
        self._island_map = self.fig.add_subplot(2, 2, 1)
        self._island_map.imshow(self.generate_map_array)
        patches = []
        for i, (landscape, l_color) in enumerate(
                self.map_colors.items()):
            patch = mpatches.Patch(color=l_color,
                                   label=self.map_labels[landscape])
            patches.append(patch)
        self._island_map.legend(handles=patches)

    def _update_count_graph(self, island_animal_count):
        herb_count, carn_count = list(island_animal_count.values())

        herb_ydata = self._herbivore_line.get_ydata()
        herb_ydata[self.year_num] = herb_count
        self._herbivore_line.set_ydata(herb_ydata)

        carn_ydata = self._carnivore_line.get_ydata()
        carn_ydata[self.year_num] = carn_count
        self._carnivore_line.set_ydata(carn_ydata)

    def _update_herb_dist(self, herb_dist):
        if self._herb_img_axis is not None:
            self._herb_img_axis.set_data(herb_dist)
        else:
            self._herb_img_axis = self._herb_dist.imshow(
                herb_dist, vmin=0,
                vmax=200,
                interpolation='nearest',
                aspect='auto',
                cmap="Spectral")
            plt.colorbar(self._herb_img_axis, ax=self._herb_dist)
            self._herb_dist.set_xticks(
                range(0, len(self.generate_map_array[0]), 5))
            self._herb_dist.set_xticklabels(range(1, 1 + len(
                self.generate_map_array[0]), 5))

            self._herb_dist.set_yticks(
                range(0, len(self.generate_map_array), 5))
            self._herb_dist.set_yticklabels(range(1, 1 + len(
                self.generate_map_array), 5))
            self._herb_dist.set_title('Herbivore distribution')

    def _update_carn_dist(self, carn_dist):
        if self._carn_img_axis is not None:
            self._carn_img_axis.set_data(carn_dist)

        else:
            self._carn_img_axis = self._carn_dist. \
                imshow(carn_dist,
                       vmin=0,
                       vmax=200,
                       interpolation='nearest',
                       aspect='auto',
                       cmap="Spectral")
            plt.colorbar(self._carn_img_axis, ax=self._carn_dist)
            self._carn_dist.set_xticks(range(0,
                                             len(self.generate_map_array[
                                                     0]), 5))
            self._carn_dist.set_xticklabels(range(1, 1 + len(
                self.generate_map_array[0]), 5))

            self._carn_dist.set_yticks(
                range(0, len(self.generate_map_array), 5))

            self._carn_dist.set_yticklabels(range(1, 1 + len(
                self.generate_map_array), 5))

            self._carn_dist.set_title('Carnivore distribution')

    def update_graphics(self):
        """This method updates the simulated graphics with the data
        provided by the Pandas DataFrame."""
        animal_count = self.animal_distribution
        row = len(self.generate_map_array)
        col = len(self.generate_map_array[0])

        self._update_count_graph(self.num_animals_per_species)

        self._update_herb_dist(
            np.array(animal_count.Herbivore).reshape(row, col))

        self._update_carn_dist(
            np.array(animal_count.Carnivore).reshape(row, col))

        plt.pause(1e-6)

        self.fig.suptitle('Year: {}'.format(self.year_num + 1), x=0.027,
                          fontsize=10)

    def save_graphics(self):
        """This method saves the simulated graphics."""
        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_nums,
                                                     type=self.img_fmt))
        self.img_nums += 1

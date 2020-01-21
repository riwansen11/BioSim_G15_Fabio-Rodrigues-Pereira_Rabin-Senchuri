# -*- coding: utf-8 -*-

"""
This is the Simulation model which functions with the BioSim package
written for the INF200 project January 2019.
"""

author = "Fábio Rodrigues Pereira and Rabin Senchuri"
email = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"

import os
import subprocess
import textwrap
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as color
from biosim.island import Island
matplotlib.use('macosx')

# update these variables to point to your ffmpeg and convert binaries
FFMPEG_BINARY = 'ffmpeg'
CONVERT_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
DEFAULT_GRAPHICS_DIR = os.path.join('..', 'data')
DEFAULT_GRAPHICS_NAME = 'BioSim'
DEFAULT_MOVIE_FORMAT = 'gif'


class BioSim:
    """Responsible to provide to the user an interface for simulation as
    well as visualization."""

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 ymax_animals=None,
                 cmax_animals=None,
                 img_base=None,
                 img_dir=DEFAULT_GRAPHICS_DIR,
                 img_name=DEFAULT_GRAPHICS_NAME,
                 img_fmt='png'):
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

        self.year_num = 0
        self.final_year = None
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

        self.img_base = os.path.join(img_dir, img_name)

        self.img_ctr = 0
        self.img_fmt = img_fmt

    @property
    def map_colors(self):
        """

        Returns
        ----------


        """
        geo_type_color = {'O': color.to_rgb('aqua'),
                          'M': color.to_rgb('darkgray'),
                          'J': color.to_rgb('forestgreen'),
                          'S': color.to_rgb('yellowgreen'),
                          'D': color.to_rgb('khaki')}

        map_compatible = textwrap.dedent(self._map).splitlines()
        map_colors = [[geo_type_color[col] for col in row]
                      for row in map_compatible]

        return map_colors

    @property
    def num_animals(self):
        """Total number of animals on island

        Returns
        ----------


        """
        pop = self.island.get_population_numbers()
        return sum(pop['herbivore']) + sum(pop['carnivore'])

    @property
    def year(self):
        """Last year simulated.

        Returns
        ----------


        """
        return self.final_year

    @property
    def num_animals_per_species(self):  # tested
        """Number of animals per species in island, as dictionary

        Returns
        ----------


        """
        pop = self.island.get_population_numbers()
        return {'herbivore': sum(pop['herbivore']),
                'carnivore': sum(pop['carnivore'])}

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island.

        Returns
        ----------


        """
        """pop = self.island.get_population_numbers()
        df = pd.DataFrame(pop)
        export_csv = df.to_csv(r'fabiorodp_biosin_data.csv',
                               index=None,
                               header=True)
        return df"""
        square_count = []

        island = self.island.cells
        for loc, geo in island.items():
            square_count.append({'x': loc[0], 'y': loc[1],
                                 'herbivores': len(geo.population[
                                                       'Herbivore']),
                                 'carnivores': len(geo.population[
                                                       'Carnivore'])})
        return pd.DataFrame(square_count, columns=['x', 'y',
                                                   'herbivores',
                                                   'carnivores'])

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

        self.final_year = self.year_num + num_years
        self._setup_graphics()

        while self.year_num < self.final_year:

            if self.num_animals is 0:
                break

            if self.year_num % vis_years is 0:
                self._update_graphics()

            if self.year_num % img_years is 0:
                self._save_graphics()

            self.island.yearly_cycle()
            self.year_num += 1

    def make_movie(self, m_fmt=DEFAULT_MOVIE_FORMAT):
        """

        Parameters
        ----------
        m_fmt: 'gif'
            DEFAULT_MOVIE_FORMAT = 'gif'
        """
        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if m_fmt is 'gif':
            try:
                subprocess.check_call([CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base,
                                                      m_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('Convert failed with: {}'.format(err))

        else:
            raise ValueError('Movie format has to be gif')

    def _setup_graphics(self):
        if self.fig is None:
            self.fig = plt.figure()
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
        self._island_map.imshow(self.map_colors, interpolation='nearest')

        self._island_map.set_xticks(
            range(0, len(self.map_colors[0]), 5))
        self._island_map.set_xticklabels(range(1, 1 + len(
            self.map_colors[0]), 5))

        self._island_map.set_yticks(
            range(0, len(self.map_colors), 5))
        self._island_map.set_yticklabels(range(1, 1 + len(
            self.map_colors), 5))

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
                range(0, len(self.map_colors[0]), 5))
            self._herb_dist.set_xticklabels(range(1, 1 + len(
                self.map_colors[0]), 5))

            self._herb_dist.set_yticks(
                range(0, len(self.map_colors), 5))
            self._herb_dist.set_yticklabels(range(1, 1 + len(
                self.map_colors), 5))
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
                                             len(self.map_colors[0]), 5))
            self._carn_dist.set_xticklabels(range(1, 1 + len(
                self.map_colors[0]), 5))

            self._carn_dist.set_yticks(
                range(0, len(self.map_colors), 5))

            self._carn_dist.set_yticklabels(range(1, 1 + len(
                self.map_colors), 5))

            self._carn_dist.set_title('Carnivore distribution')

    def _update_graphics(self):
        animal_count = self.animal_distribution
        row, col = len(self.map_colors), len(self.map_colors[0])

        self._update_count_graph(self.num_animals_per_species)

        self._update_herb_dist(
            np.array(animal_count.herbivores).reshape(row, col))

        self._update_carn_dist(
            np.array(animal_count.carnivores).reshape(row, col))

        plt.pause(1e-6)

        self.fig.suptitle('Year: {}'.format(self.year_num + 1), x=0.105)

    def _save_graphics(self):
        if self.img_base is None:
            return
        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_ctr,
                                                     type=self.img_fmt))
        self.img_ctr += 1

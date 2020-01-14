# -*- coding: utf-8 -*-

"""
This is the geography model which functions with the BioSim package 
written for the INF200 project January 2019.
"""

__author__ = "Fábio Rodrigues Pereira and Rabin Senchuri"
__email__ = "fabio.rodrigues.pereira@nmbu.no and rabin.senchuri@nmbu.no"


class Geography:
    """
    Here there are methods useful to identify and organize and check
    restrictions when a geography of any region is given.

    Also creates geography parameters objects
    """
    geo_types = {'O': 'Ocean', 'S': 'Savannah', 'M': 'Mountain',
                 'J': 'Jungle', 'D': 'Desert'}

    @staticmethod
    def list_geo_cells(geogr):
        return [list(row.strip()) for row in geogr]

    def __init__(self, geogr):
        self.geogr = self.list_geo_cells(geogr)
        self.check_line_lengths()
        self.check_invalid_character()
        self.check_invalid_boundary()

    def check_line_lengths(self):
        length_count = [len(row) for row in self.geogr]
        for i in length_count:
            if i is not length_count[0]:
                raise ValueError('Different line lengths detected')

    def check_invalid_character(self):
        for row in self.geogr:
            for letter in row:
                if letter not in self.geo_types.keys():
                    raise ValueError('Invalid character identified')

    def check_invalid_boundary(self):
        for north in self.geogr[0]:
            for south in self.geogr[-1]:
                if north is not 'O' or south is not 'O':
                    raise ValueError('The boundary is not Ocean')
        for row in self.geogr:
            west, east = row[0], row[-1]
            if west is not 'O' or east is not 'O':
                raise ValueError('The boundary is not Ocean')

    def cells(self):
        loc = [(i, j) for i in range(len(self.geogr))
               for j in range(len(self.geogr[0]))]
        geo = [geo for i in range(len(self.geogr))
               for geo in self.geogr[i]]
        return dict(zip(loc, geo))

    def find_landscape_type(self, landscape):
        """
        Finds any landscape default parameter.

        :param landscape: string
        """
        if landscape in self.geo_types.keys():
            return self.geo_types[landscape]
        else:
            raise ValueError('Geography {} not found'.format(landscape))

    def set_parameters(self, landscape=None, params=None):
        """
        Updates any landscape parameter.

        :param landscape: string
        :param params: dict
        """
        if not isinstance(params, dict):
            raise TypeError("'param_dict' must be type 'dict'")

        else:
            geo = self.find_landscape_type(landscape)
            for parameter in params.keys():
                if 'f_max' is parameter and params['f_max'] <= 0:
                    raise ValueError(
                        "parameter 'f_max' must be non-negative")
                elif parameter not in geo.parameters.keys():
                    raise ValueError(
                        "unknown parameter: '{}'".format(parameter))
            geo.parameters.update(params)


class Jungle(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': 800.0, 'alpha': None}


class Savannah(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': 300.0, 'alpha': 0.3}


class Desert(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}


class Ocean(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}


class Mountain(Geography):
    def __init__(self):
        super().__init__()
        self.parameters = {'f_max': None, 'alpha': None}

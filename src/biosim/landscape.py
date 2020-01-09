from src.biosim.animals import Animal
from src.biosim.animalOgen import AnimalObject
from operator import attrgetter


class Tile:
    """
    A single tile representation of whole island
    """
    habitable = False

    def __init__(self, loc):
        """
            Parameters
            ----------
                loc: tuple
                    tuple with two coordinates
        """
        self.loc = loc
        self.list_herb = []
        self.herb_pop = []
        self.fodder = 0

    @classmethod
    def set_landscape_parameters(cls, params=None):
        """
        Sets user-defined simulation parameters for all squares pertaining to
        the Square superclass.

        Parameters
        ----------
        params: dict
            Dictionary with parameters to be changed, must be a subset of
            default parameters.

        """
        if not isinstance(params, dict):
            raise TypeError("'param_dict' must be type 'dict'")

        for parameter in params.keys():
            if parameter not in cls.default_params.keys():
                raise ValueError(
                    "unknown parameter: '{}'".format(parameter))
        if 'f_max' in params.keys():
            if not 0 <= params['f_max']:
                raise ValueError(
                    "parameter 'f_max' must be non-negative")
        cls.default_params.update(params)

    def num_herbs(self):
        """
            Returns
            -------
                int
                    Number of herbivores in each cell
        """
        return len(self.list_herb)


    def add_herb(self, animal):
        """Add herbivore to each cell

            Parameters
            ----------
                animal: list
                    list of animals

            Returns
            -------
                list
                    list of herbivores
        """

        for i in range(len(animal)):
            if animal[i]['loc'] == self.loc:
                self.list_herb.append(animal[i])
        ao = AnimalObject(self.list_herb)
        self.list_herb = ao.animal_object()


    def aging(self):
        """
            Returns
            -------
                int
                    age of each animal

        """
        for a in self.list_herb:
            a.ages()


    def loose_weight(self):
        """
            Returns
            -------
                int
                    amount of weight lost
        """

        for a in self.list_herb:
            a.weight_decrease()



    def death(self):
        """
             Returns
             -------
                list
                    Survivors list of animals for each species
        """
        survivors_herb = []

        for a in self.list_herb:
            if not a.death():
                survivors_herb.append(a)
        self.list_herb = survivors_herb


    def birth(self):
        """Gives the list of newborn herbivore and carnivore animals

            Returns
            -------
                list
                    list newborn herbivore and carnivore animals

        """
        newborn_herb = []
        n = len(self.list_herb)
        for a in self.list_herb:
            h_baby = a.birth(n)
            if h_baby:
                newborn_herb.append(h_baby)
        self.list_herb.extend(newborn_herb)


    def h_feed(self):
        """Gives the amount of food eating by herbivore

            Returns
            -------
                int
                    amount of fodder eaten by herbivore
        """
        self.list_herb.sort(key=lambda a: a.fitness)
        for herb in reversed(self.list_herb):
            eaten = herb.h_eating_rule(self.fodder)
            self.fodder -= eaten


class Ocean(Tile):
    """Gives a tile of Ocean"""
    pass


class Mountain(Tile):
    """Gives a tile of Mountain"""
    pass


class Desert(Tile):
    """Gives a tile of Desert"""
    habitable = True

    def __init__(self, loc):
        """Gives a superclass of location"""
        super().__init__(loc)

    def grow(self):
        """Amount of food grown in Desert

            Returns
            -------
                int
                    amount of food available in the Desert cell
        """
        self.fodder = 0


class Savannah(Tile):
    """Gives a tile of Savannah"""
    habitable = True
    default_params = {'f_max': 300, 'alpha': 0.3}
    alpha = default_params['alpha']

    f_max = default_params['f_max']

    def __init__(self, loc):
        """
            Parameters
            ----------
                loc: tuple
                    tuple with two coordinates

        """
        super().__init__(loc)
        self.fodder = self.f_max


    def grow(self):
        """Gives the amount of food available in Savannah cell
            Returns
            -------
                int
                    amount of food available in the cell

        """
        self.fodder = self.fodder + self.alpha * (self.f_max - self.fodder)


class Jungle(Tile):
    """Gives a tile of Jungle"""
    habitable = True
    default_params = {'f_max': 800}

    f_max = default_params['f_max']

    def __init__(self, loc):
        """
            Parameters
            ----------
            loc: tuple
                tuple of two coordinates
        """
        super().__init__(loc)
        self.fodder = self.f_max

    def grow(self):
        """Gives the amount of food available in Jungle cell"""
        self.fodder = self.f_max

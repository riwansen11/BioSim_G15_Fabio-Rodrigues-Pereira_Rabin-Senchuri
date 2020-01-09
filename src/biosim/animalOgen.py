from src.biosim.animals import Herbivore



class AnimalObject():

    """Creates herbivore and carnivore animals object
       """
    def __init__(self, list_herb):
        """

        Parameters
        ----------
        animal: int
            gives the list of animals
        """
        self.list_herb = list_herb
        self.animal_pop = []


    def animal_object(self):

        """
       Returns
       -------
           tuple
               Herbivore and Carnivore list with age and weight
       """
        animal = []
        for i in range(len(self.list_herb)):
            animal.append(self.list_herb[i]['pop'])
        for a in range(len(animal)):
            for j in range(len(animal[a])):
                if animal[a][j]['species'] == "Herbivore":
                    self.animal_pop.append(Herbivore(animal[a][j]['age'],
                                                   animal[a][j]['weight']))
        print(self.animal_pop)
        return self.animal_pop


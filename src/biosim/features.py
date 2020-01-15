from src.biosim.geography import Geography
from src.biosim.fauna import Fauna


class Vectors:
    def __init__(self, cells, population):
        self.population = population
        self.pop_cells_vector = cells
        self.pop_herb_cells_vector = []
        self.pop_carn_cells_vector = []

    def creates_empty_cells(self):
        for rownum, row in enumerate(self.pop_cells_vector):
            for colnum, col in enumerate(row):
                self.pop_cells_vector[rownum][colnum] = []
        return self.pop_cells_vector

    def vectorizer_population(self):
        for d in self.population:
            lista, rownum, colnum = [], d['loc'][0], d['loc'][1]
            for e in d['pop']:
                lista.append(list(e.values()))
            self.pop_cells_vector[rownum][colnum].extend(lista)
        return self.pop_cells_vector

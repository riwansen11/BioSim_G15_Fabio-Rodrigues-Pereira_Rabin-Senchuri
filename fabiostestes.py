from biosim.simulation import BioSim
from biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert
from biosim.fauna import Population, Herbivore, Carnivore

island_map = '''OOOOO\nODDJO\nOJJJO\nOJJJO\nOOOOO'''

ini_herbs = [{"loc": (2, 3),
              "pop": [{"species": "Herbivore", "age": 5, "weight": 40}
                      for _ in range(150)], }]

ini_carns = [{"loc": (2, 3),
              "pop": [{"species": "Carnivore", "age": 5, "weight": 40}
                      for _ in range(40)], }]

t = BioSim(island_map, ini_herbs, 1)
t.set_animal_parameters("Herbivore", {"zeta": 3.2, "xi": 1.8})
t.set_animal_parameters("Carnivore", {"a_half": 70,
                                      "phi_age": 0.5,
                                      "omega": 0.3,
                                      "F": 65,
                                      "DeltaPhiMax": 9.0, }, )
t.set_landscape_parameters("J", {"f_max": 700})
print(t.animal_distribution)

a = 1
while a < 5:
    t.simulate(10)
    print(t.island.cells[(2, 3)].parameters)
    print(t.animal_distribution)
    print(t.island.cells[(2, 3)].parameters)
    a += 1

t.add_population(ini_carns)

b = 1
print(t.animal_distribution)
while b < 10:
    t.simulate(10)
    print(t.animal_distribution)
    b += 1

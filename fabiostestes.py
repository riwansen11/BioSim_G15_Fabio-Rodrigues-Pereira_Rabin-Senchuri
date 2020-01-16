from src.biosim.fauna import Population, Herbivore, Carnivore
from src.biosim.simulation import BioSim
from src.biosim.geography import Ocean, Savannah, Mountain, Jungle, \
    Desert

ini_pop = [
    {
        "loc": (5, 7),
        "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (5, 7),
        "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (5, 7),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (5, 7),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (5, 7),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    }
]
a = BioSim(None, ini_pop, None)
loc = (5, 7)
'''for a, b in enumerate(a.island.cells.items()):
    print(a)
    print(b)'''
a.island.feeding()
print(a.island.cells.items())
print(a.island.cells.keys())
print(a.island.cells.values())
print(a.island.habitable_cells)






''' >> dict.items()
dict_items([((0, 0), 
<src.biosim.geography.Ocean object at 0x10f697c90>), ...
>> for coordinates, geo_object in dict.items():
(0, 0) <src.biosim.geography.Ocean object at 0x10f697c90>'''

'''island_map = "OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"
ini_pop = [
    {
        "loc": (2, 2),
        "pop": [{"species": "Herbivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (2, 3),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (2, 1),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (1, 2),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    },
    {
        "loc": (3, 2),
        "pop": [{"species": "Carnivore", "age": 5, "weight": 20}],
    }
]

a = BioSim(island_map, ini_pop, None)
loc = (2, 2)
b = tuple(a.island.habitable_geos.values())
c = a.island.cells.items()
print(c)

for coordinates, geo_object in c:
    print(coordinates, geo_object)
    if isinstance(geo_object, b):
        print(b)
        print(geo_object)
        print(True)'''

# print(Herbivore)
'''<class 'src.biosim.fauna.Herbivore'>'''

# print(type(Herbivore))
'''<class 'type'>'''

# print(a.island.cells[loc])
'''<src.biosim.geography.Jungle object at 0x114a0ad90>'''

# print(type(a.island.cells[loc]))
'''<class 'src.biosim.geography.Jungle'>'''

# print(a.island.cells[loc].population)
'''{<class 'src.biosim.fauna.Herbivore'>: 
[<src.biosim.fauna.Herbivore object at 0x10cf36050>], 
<class 'src.biosim.fauna.Carnivore'>: []}'''

# print(type(a.island.cells[loc].population))
'''<class 'dict'>'''

'''[<src.biosim.geography.Jungle object at 0x10d696a90>, ...,
<src.biosim.geography.Jungle object at 0x10d696b10>]'''

# print(a.island.habitable_geos.keys())
'''dict_keys(['S', 'J', 'D'])'''


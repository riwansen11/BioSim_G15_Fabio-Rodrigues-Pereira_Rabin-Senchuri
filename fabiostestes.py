from src.biosim.simulation import BioSim

island_map = "OOOOO\nOJJJO\nOJJJO\nOJJJO\nOOOOO"
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
print(a.island.habitable_geos.values())
'''[<src.biosim.geography.Jungle object at 0x10d696a90>, ...,
<src.biosim.geography.Jungle object at 0x10d696b10>]'''



import textwrap
from src.biosim.simulation import BioSim
from src.biosim.fauna import Herbivore, Carnivore

ini_pop = [
        {
            "loc": (1, 14),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
            ],
        }
    ]

a = BioSim(None, ini_pop, None)

loc = (1, 14)
print(a.island.habitable_geos.values())

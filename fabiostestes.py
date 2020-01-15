import textwrap
from src.biosim.simulation import BioSim

ini_pop = [
        {
            "loc": (2, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
            ],
        }
    ]

a = BioSim(None, ini_pop, None)


print(a.island.cells)

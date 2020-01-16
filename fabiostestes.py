from src.biosim.simulation import BioSim

ini_pop = [
        {
            "loc": (1, 14),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20},
                {"species": "Herbivore", "age": 10, "weight": 20},
                {"species": "Carnivore", "age": 2, "weight": 20}
            ],
        }
    ]

a = BioSim(None, ini_pop, None)

loc = (1, 14)
b = a.island.cells[loc].population
for species in b.values():
    print(species)
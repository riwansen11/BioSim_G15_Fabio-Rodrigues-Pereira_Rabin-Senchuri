from src.biosim.simulation import BioSim
import numpy as np


loc = (9, 9)
pop_data = {"species": "Carnivore", "age": 5, "weight": 20}

population = [{
    "loc": (10, 10),
    "pop": [
        {"species": "Herbivore", "age": 5, "weight": 20}
        for _ in range(5)
    ],
},
    {
        "loc": (10, 10),
        "pop": [
            {"species": "Carnivore", "age": 5, "weight": 20}
            for _ in range(2)
        ],
    }]

if True:
    population.append({"loc": loc, "pop": []})
    population[-1]["pop"].append(pop_data)

print(population)

for i in population:
    loc, pop = i['Loc'], i['pop']

    for pop_data in pop:
        if pop_data['species'] is 'Herbivore':
            Herbivore.population(loc, pop_data)
        else:
            Carnivore.population(loc, pop_data)




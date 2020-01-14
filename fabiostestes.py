from src.biosim.simulation import BioSim
import numpy as np

ini_herbs = [
        {
            "loc": (10, 10),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(150)
            ],
        }
    ]

a = BioSim(None, ini_herbs, None)
b = a.geography.cells

for element in b:
    print(element[0])
    if element[0] != 'O':
        raise ValueError('error')





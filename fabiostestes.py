from src.biosim.landscape import Map

c = Map()
island_map = c.coordinations()

a = [(island_map[rownum][colnum])
     for rownum, row in enumerate(island_map)
     for colnum, itemvalue in enumerate(row)
    ]

print(a)

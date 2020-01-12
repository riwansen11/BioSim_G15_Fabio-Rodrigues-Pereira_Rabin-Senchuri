a = ('w_birth', 'sigma_birth', 'beta', 'eta', 'a_half', 'phi_age',
     'w_half', 'phi_weight', 'mu', 'lambda', 'gamma', 'zeta', 'xi',
     'omega', 'F', 'DeltaPhiMax')

c = {'Herbivore': (8.0, 1.5, 0.9, 0.05, 40.0, 0.2, 10.0,
                   0.1, 0.25, 1.0, 0.2, 3.5, 1.2, 0.4,
                   10.0, None),
     'Carnivore': (777.0, 1.5, 0.9, 0.05, 40.0, 0.2, 10.0,
                   0.1, 0.25, 1.0, 0.2, 3.5, 1.2, 0.4,
                   10.0, None),
     'J': (800.0, None),
     'S': (300.0, 0.3)
     }

"""b = (8.0, 1.5, 0.9, 0.05, 40.0, 0.2, 10.0, 0.1, 0.25, 1.0, 0.2, 3.5,
     1.2, 0.4, 10.0)"""

print(dict(zip(a, c['Carnivore'])))

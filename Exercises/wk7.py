import quantities as pq

mass_h2o = 5 * pq.gram
molar_mass_h2o = 18.01 * (pq.gram) / (pq.mol)
mol_h2o = mass_h2o / molar_mass_h2o
print(round(mol_h2o, 2))

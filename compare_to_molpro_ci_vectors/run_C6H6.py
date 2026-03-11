from compare_to_molpro_ci_vectors.help_functions.compare_different_dimers import compare_different_dimers
from compare_to_molpro_ci_vectors.help_functions.make_hashable import make_hashable
from src.symmetries.Molecule import Molecule



tables_by_molecule = {}


# Testing :
print("C6H6:")
tables_C6H6 = compare_different_dimers(molecule_of_theory=Molecule.C6H6, molecule_of_molpro="C6H6")
tables_by_molecule["C6H6"] = list(tables_C6H6.values())[-1]

print("==="*50, "\n")

print("C4H4N2:")
tables_C4H4N2 = compare_different_dimers(molecule_of_theory=Molecule.C6H6, molecule_of_molpro="C4H4N2")
tables_by_molecule["C4H4N2"] = list(tables_C4H4N2.values())[-1]

print("==="*50, "\n")

print("C6Cl6:")
tables_C6Cl6 = compare_different_dimers(molecule_of_theory=Molecule.C6H6, molecule_of_molpro="C6Cl6")
tables_by_molecule["C6Cl6"] =  list(tables_C6Cl6.values())[-1]

print("==="*50, "\n")

print("C6F6:")
tables_C6F6 = compare_different_dimers(molecule_of_theory=Molecule.C6H6, molecule_of_molpro="C6F6")
tables_by_molecule["C6F6"] = list(tables_C6F6.values())[-1]



print("\n"*6, "***"*50, "\n")


# Group molecules by identical tables
table_groups = {}
for mol, table in tables_by_molecule.items():
    key = make_hashable(table)
    if key not in table_groups:
        table_groups[key] = {"molecules": [mol], "table": table}
    else:
        table_groups[key]["molecules"].append(mol)

# Print the results
for group in table_groups.values():
    mol_list = " & ".join(group["molecules"])
    print(f"{mol_list}:\n", group["table"], "\n", sep="\n")

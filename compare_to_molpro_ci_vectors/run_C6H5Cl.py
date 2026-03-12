from compare_to_molpro_ci_vectors.help_functions.compare_different_dimers import compare_different_dimers
from compare_to_molpro_ci_vectors.help_functions.make_hashable import make_hashable
from src.symmetries.Molecule import Molecule



tables_by_molecule = {}


# Testing :
print("C6H5Cl:")
tables_C6H5Cl = compare_different_dimers(molecule_of_theory=Molecule.C6H5Cl, molecule_of_molpro="C6H5Cl", ci_vector_dismiss_limit=0.2)
tables_by_molecule["C6H5Cl"] = list(tables_C6H5Cl.values())[-1]

print("==="*50, "\n")

print("C5H5N:")
tables_C5H5N = compare_different_dimers(molecule_of_theory=Molecule.C5H5N, molecule_of_molpro="C5H5N", ci_vector_dismiss_limit=0.3)
tables_by_molecule["C5H5N"] = list(tables_C5H5N.values())[-1]

print("==="*50, "\n")



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

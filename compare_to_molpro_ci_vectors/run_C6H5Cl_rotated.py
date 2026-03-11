from compare_to_molpro_ci_vectors.help_functions.compare_different_dimers import compare_different_dimers
from compare_to_molpro_ci_vectors.help_functions.make_hashable import make_hashable
from src.symmetries.Molecule import Molecule



tables_by_molecule = {}


# Testing :
print("C6H5Clrotated:")
tables_C6H5Clrotated = compare_different_dimers(molecule_of_theory=Molecule.C6H5Cl_rotated, molecule_of_molpro="C6H5Clrotated", ci_vector_dismiss_limit=0.2)
tables_by_molecule["C6H5Clrotated"] = list(tables_C6H5Clrotated.values())[-1]


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

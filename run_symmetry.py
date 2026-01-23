from symmetries.Molecule import Molecule
from symmetries.all_products import all_products
from symmetries.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from symmetries.linear_combinations.linear_combinations_of_combined_monomer_states import \
    linear_combinations_of_combined_monomer_states
from symmetries.latex.get_latex_file_for_all_combinations import get_latex_file_for_d2h_symmetry_options


if __name__ == "__main__":
    detailed = True
    # detailed = False

    for molecule in [
        Molecule.C6H6,
        Molecule.C6H5Cl,
        Molecule.C6H5Cl_rotated
    ]:
        content = all_products(molecule=molecule, monomer_combinations=True, detailed=detailed)
        content += all_products(molecule=molecule,monomer_combinations=False,detailed=detailed)
        content += get_monomer_state_linear_combinations(molecule=molecule, detailed=detailed)[0]
        content += linear_combinations_of_combined_monomer_states(molecule=molecule, detailed=detailed)
        get_latex_file_for_d2h_symmetry_options(content, molecule=molecule)
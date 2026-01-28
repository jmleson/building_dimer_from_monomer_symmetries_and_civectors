from CI_Vectors.get_product_terms import get_product_terms
from Molecule import Molecule
from get_linear_combined_states_results import get_linear_combined_states_results
from latex.basic_latex_header import basic_latex_header
from orbitals_and_their_symmetry_chapter import orbitals_and_their_symmetry_chapter


def get_file_ci_vectors(molecule:Molecule):
    content = basic_latex_header()
    content += orbitals_and_their_symmetry_chapter(molecule=molecule)

    content += get_product_terms(molecule=molecule)
    content += "\n" + r"\newpage" + "\n"
    content += get_linear_combined_states_results(molecule=molecule, print_ci_vectors=True, print_symmetries=False)

    end= r"\end{document}"
    with open(f"resulting_tex_files/CI-vektoren-theoretisch_{molecule.name}.tex", "w") as file:
        file.write(content + end)




if __name__ == "__main__":
    molecule = Molecule.C6H6
    get_file_ci_vectors(molecule=molecule)
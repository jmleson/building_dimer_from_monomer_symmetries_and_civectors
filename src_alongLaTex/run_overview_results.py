from src_alongLaTex.Molecule import Molecule
from src_alongLaTex.get_linear_combined_states_results import get_linear_combined_states_results
from src_alongLaTex.get_monomer_states_and_configurations import get_monomer_states_and_configurations
from src_alongLaTex.latex.basic_latex_header import basic_latex_header
from src_alongLaTex.orbitals_and_their_symmetry_chapter import orbitals_and_their_symmetry_chapter


def run_overview_results(molecule:Molecule):
    content = basic_latex_header()

    content += orbitals_and_their_symmetry_chapter(molecule=molecule)

    content += get_monomer_states_and_configurations(molecule=molecule)

    content += get_linear_combined_states_results(molecule=molecule, print_symmetries=True, print_ci_vectors=True)

    end = r"\end{document}"
    with open(f"src_alongLaTex/resulting_tex_files/{molecule.name}.tex", "w") as file:
        file.write(content + end)


if __name__ == "__main__":
    molecule = Molecule.C6H6
    run_overview_results(molecule=molecule)
from Molecule import Molecule
from get_linear_combined_states_results import get_linear_combined_states_results
from latex.basic_latex_header import basic_latex_header



def run_overview_results(molecule:Molecule):
    content = basic_latex_header()

    content += get_linear_combined_states_results(molecule=molecule, print_symmetries=True, print_ci_vectors=True)

    end = r"\end{document}"
    with open(f"resulting_tex_files/{molecule.name}.tex", "w") as file:
        file.write(content + end)


if __name__ == "__main__":
    molecule = Molecule.C6H6
    run_overview_results(molecule=molecule)
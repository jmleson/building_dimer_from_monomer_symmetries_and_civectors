from src_alongLaTex.Molecule import Molecule
from src_alongLaTex.get_monomer_states_and_configurations import get_monomer_states_and_configurations
from src_alongLaTex.latex.basic_latex_header import basic_latex_header
from src_alongLaTex.orbitals_and_their_symmetry_chapter import orbitals_and_their_symmetry_chapter


def get_latex_file_for_d2h_symmetry_options(content:str, molecule:Molecule) -> None :
    """
    writing a latex file with all given content, that is able to compile tikz-figures as well as equations
    :param content: content of to-be latex file
    :return:
    """
    start = basic_latex_header()

    chapter1 = orbitals_and_their_symmetry_chapter(molecule=molecule)

    chapter2 = get_monomer_states_and_configurations(molecule=molecule)

    end= r"\end{document}"
    with open(f"resulting_tex_files/{molecule.value}_{molecule.get_point_group().value}.tex", "w") as file:
        file.write(start
                   + chapter1
                   + chapter2
                   + content
                   + end)




from src.Molecule import Molecule
from src.latex.basic_latex_header import basic_latex_header
from src.latex.pdf_summary.orbitals_and_their_symmetry_chapter import orbitals_and_their_symmetry_chapter


def get_summarizing_latex_file(molecule:Molecule):
    """
        writing a latex file with all given content, that is able to compile tikz-figures as well as equations
        :param content: content of to-be latex file
        :return:
        """
    start = basic_latex_header()

    chapter1 = orbitals_and_their_symmetry_chapter(molecule=molecule)

    # chapter2 = get_monomer_states_and_configurations(molecule=molecule)

    end = r"\end{document}"
    with open(f"src/resulting_tex_files/{molecule.value}_{molecule.get_point_group().value}.tex", "w") as file:
        file.write(start
                   + chapter1
                   # + chapter2
                   # + content
                   + end)


if __name__ == '__main__':
    tikz = get_summarizing_latex_file(Molecule.C6H6)
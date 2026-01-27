from Molecule import Molecule
from latex.basic_latex_header import basic_latex_header
from latex.format_irred_representations import format_irred_representations
from symmetries.general_functionalities.monomer_positions import MonomerPositions
from get_mo_schema import get_mo_schemata, wrap_tikzpicture


def get_latex_file_for_d2h_symmetry_options(content:str, molecule:Molecule) -> None :
    """
    writing a latex file with all given content, that is able to compile tikz-figures as well as equations
    :param content: content of to-be latex file
    :return:
    """
    start = basic_latex_header() + r"\section{Orbitals And Their Symmetry}%Orbitale und deren Symmetrie "  + "\n"

    chapter1, molecule = orbitals_and_their_symmetry_chapter(molecule=molecule)


    end= r"\end{document}"
    with open(f"resulting_tex_files/{molecule.value}_{molecule.get_point_group().value}.tex", "w") as file:
        file.write(start
                   + chapter1
                   + content
                   + end)



def orbitals_and_their_symmetry_chapter(molecule:Molecule):
    point_group = molecule.get_point_group()
    start = ""
    # if point_group == POINTGROUP.D2h:
    #     start += r"%In der Sortierung: oben rechts $a_u$, oben links $b_{1u}$, unten links $b_{2g}$ und unten rechts $b_{3g}$ folgt: \\"
    # elif point_group == POINTGROUP.C2v or point_group == POINTGROUP.C2h:
    #     start += r"%In der Sortierung: oben rechts $ $, oben links $ $, unten links $ $ und unten rechts $ $ folgt: \\"
    # else:
    #     raise Exception("unknown molecule for point group")

    filename = molecule.get_info_file()
    if filename is not None and len(filename) > 0:
        start += "\n" + r"%\includegraphics[scale=0.125]{img/" + filename + r"}" + "\n"
        start += r"\vspace{2cm}" + "\n"

    empty_mos = {value: {MonomerPositions.left: 0, MonomerPositions.right: 0} for value in point_group.label.values()}
    labeled_monomer_orbitals = wrap_tikzpicture(get_mo_schemata(occupied_mos=empty_mos, monomer=MonomerPositions.isolated, point_group=point_group))
    unlabeled_monomer_orbitals = labeled_monomer_orbitals.replace("node", "%node")

    start += "We use the following order of orbitals here (assuming degeneracy of LUMOs and HOMOs): "+ "\n"
    start += "$$" + "\n" + labeled_monomer_orbitals + "\n" + "$$" + "\n"
    start += "In the following, we will leave out the explicit labeling by orbital symmetry. Each monomer will simply be written as:\n"
    start +=  "$$" + "\n" + unlabeled_monomer_orbitals + "\n" + "$$" + "\n"
    start += "where the character of the orbital is defined by its position. \n\n"
    start += ("Dimer configurations will be written as their monomer occupations, by writing one monomer to the left and one to the right. "
              "The orbital order within the group of monomer orbitals follows the above mentioned definition. ")


    start += r"\vspace{2cm}"
    start += " The transformation of monomer orbitals into dimer orbitals is given by knowing the negative and positive linera combinations of monomer orbitals into dimer orbitals. "
    start += "Transforming this known equation system leads to: " + "\n"
    start += r"\begin{subequations}\begin{gather}" + "\n"
    combination_str = r"  \\" + "\n"
    start += combination_str.join( [format_irred_representations(monomer) + " = " + format_irred_representations(combination)
                                        for monomer, combination in point_group.mo_pairs.items() ] )
    start += r"\end{gather}\end{subequations}" + "\n"

    return start, molecule


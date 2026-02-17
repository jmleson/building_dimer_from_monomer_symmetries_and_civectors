from src.Molecule import Molecule
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.latex.format_irred_representations import format_irred_representations
from src.latex.latex_equation_types import get_expression_as_latex_formula, latex_equation_types
from src.latex.wrap_tikz_picture import wrap_tikz_picture


def orbitals_and_their_symmetry_chapter(molecule:Molecule):
    point_group = molecule.get_point_group()
    start = r"\section{Orbitals And Their Symmetry}%Orbitale und deren Symmetrie "  + "\n"
    monomer_occupation = MonomerOccupation(point_group=point_group)

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

    monomer_with_labels = wrap_tikz_picture(monomer_occupation.latex_picture(draw_label=True))
    monomer_with_labels = get_expression_as_latex_formula( monomer_with_labels, latex_equation_types.DISPLAYED)

    monomer_simple = wrap_tikz_picture(monomer_occupation.latex_picture(draw_label=False))
    monomer_simple = get_expression_as_latex_formula(monomer_simple, latex_equation_types.DISPLAYED)

    start += "We use the following ordering of orbitals here (assuming degeneracy of LUMOs and HOMOs): "+ "\n"
    start += "\n" + monomer_with_labels + "\n"
    start += "In the following, we will leave out the explicit labeling by orbital symmetry. Each monomer will simply be written as:\n"
    start +=  "\n" + monomer_simple  + "\n"
    start += "where the character of the orbital is defined by its position. " + r"\\ \\ " + "\n\n\n"
    start += ("Dimer configurations will be written as their monomer occupations, by writing one monomer to the left and one to the right. "
              "The orbital ordering within the group of monomer orbitals follows the above mentioned definition. ")
    start += r"\\ \\"
    start += " The transformation of monomer orbitals into dimer orbitals is given by knowing the negative and positive linear combinations of monomer orbitals into dimer orbitals. "
    start += "Transforming this known equation system leads to: " + "\n"

    combination_str = r"  \\" + "\n"
    equations = combination_str.join( [format_irred_representations(monomer) + " = " + format_irred_representations(combination)
                                        for monomer, combination in point_group.mo_pairs.items() ] )
    combination_str = get_expression_as_latex_formula(equations, latex_equation_types.SUBEQ)
    start += combination_str + "\n"

    return start + r"\newpage" + "\n\n"



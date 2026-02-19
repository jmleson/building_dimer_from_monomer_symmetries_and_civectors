from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.latex.pdf_summary.get_summarizing_latex_file import get_summarizing_latex_file


order = CI_ORDERING.my



tikz = get_summarizing_latex_file(Molecule.C6H6, ordering=order, detailed=True)
tikz = get_summarizing_latex_file(Molecule.C6H6, ordering=order, detailed=False)

tikz = get_summarizing_latex_file(Molecule.C6H5Cl, ordering=order, detailed=False)
tikz = get_summarizing_latex_file(Molecule.C6H5Cl_rotated, ordering=order, detailed=False)

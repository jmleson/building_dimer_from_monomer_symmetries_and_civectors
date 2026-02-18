from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.latex.pdf_summary.get_summarizing_latex_file import get_summarizing_latex_file



tikz = get_summarizing_latex_file(Molecule.C6H6, ordering=CI_ORDERING.molpro, detailed=False)
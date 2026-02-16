from src.CI_ORDERING import CI_ORDERING
from src.Molecule import Molecule
from src.latex.latex_equation_types import latex_equation_types, get_expression_as_latex_formula


def get_monomer_states_and_configurations(molecule:Molecule, order:CI_ORDERING):
    start = r"\section{Monomer States and Configurations} "  + "\n"
    point_group = molecule.get_point_group()

    # CASCI-Information about Monomer-CI's:
    triplet_states = molecule.get_ci_vectors_triplets()
    for triplet_sym in triplet_states:
        eq = triplet_sym.to_latex(order=order)
        start += get_expression_as_latex_formula(eq, latex_equation_types.BASIC) + "\n"

    return start + r"\newpage" + "\n\n"
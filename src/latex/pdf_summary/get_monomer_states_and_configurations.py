from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.latex.latex_equation_types import latex_equation_types, get_expression_as_latex_formula


def get_monomer_states_and_configurations(molecule:Molecule, ordering:CI_ORDERING):
    start = r"\section{Monomer States and Configurations} "  + "\n"

    # CASCI-Information about Monomer-CI's:
    monomer_states = molecule.get_ci_vectors_triplets()
    for triplet_sym in monomer_states:
        eq = triplet_sym.to_latex(ordering=ordering, multiplied_out=False, short_version=False)
        start += get_expression_as_latex_formula(eq, latex_equation_types.BASIC) + "\n"

    return start + r"\newpage" + "\n\n"
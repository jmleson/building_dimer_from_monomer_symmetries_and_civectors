from src.latex.latex_equation_types import latex_equation_types, get_expression_as_latex_formula
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states



def get_dimer_states_and_configurations(molecule:Molecule, ordering:CI_ORDERING, detailed:bool):
    start = r"\section{Linear Combinations} " + "\n"

    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule, ordering=ordering)
    for d in dimer_states:
        d.get_product_terms()
        start += "\n" + r"\subsection{\boldmath "+ get_expression_as_latex_formula(d.get_label(),latex_equation_types.INLINE) + r"}" +"\n"
        start += d.to_latex(detailed=detailed) + "\n"
        start += "\n" + r"\vspace{0.5cm}" if detailed else r"\newpage" + "\n"

    return start + r"\newpage" + "\n\n"

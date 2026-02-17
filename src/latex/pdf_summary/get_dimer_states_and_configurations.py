from src.CI_ORDERING import CI_ORDERING
from src.Molecule import Molecule
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.latex.minipage import minipage


def get_dimer_states_and_configurations(molecule:Molecule, ordering:CI_ORDERING, detailed:bool):
    start = r"\section{Linear Combinations} " + "\n"

    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule, ordering=ordering)
    for d in dimer_states:
        d.get_product_terms()
        if not detailed:
            start += minipage( d.to_latex(detailed=detailed)  + "\n" )
        else:
            start += d.to_latex(detailed=detailed) + "\n"
        start += r"\hrule" + "\n" + r"\vspace{0.5cm}" + "\n"


    return start + r"\newpage" + "\n\n"

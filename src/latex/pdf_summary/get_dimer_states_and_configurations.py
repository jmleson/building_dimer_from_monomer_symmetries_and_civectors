from src.CI_ORDERING import CI_ORDERING
from src.Molecule import Molecule
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.latex.minipage import minipage


def get_dimer_states_and_configurations(molecule:Molecule, ordering:CI_ORDERING):
    start = r"\section{Linear Combinations} " + "\n"

    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule)
    for d in dimer_states:
        d.get_product_terms()
        start += minipage( d.to_latex(ordering=ordering, detailed=True)  + "\n" )
        start += r"\hrule" + "\n" + r"\vspace{0.5cm}" + "\n"



    return start + r"\newpage" + "\n\n"


from src.CI_ORDERING import CI_ORDERING
from src.Molecule import Molecule
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.latex.get_table import get_table


def get_overview_table_for_civectors(molecule:Molecule, ordering:CI_ORDERING) -> str:
    start = r"\section{CI Vector Conclusion} " + "\n"

    table = ["Dimer State & CI Vectors"]
    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule, ordering=ordering)
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()
        table.append(fr"\hline ${d.get_label()} \displaystyle $ & $ {d.written_in_dimer_ci_vectors(summed_up=True, short_version=True)} \displaystyle $")


    return start + get_table(content_lines=table, number_of_columns=2, break_line_distance=1) + "\n\n"
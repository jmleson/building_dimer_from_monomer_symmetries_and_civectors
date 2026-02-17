from src.CI_ORDERING import CI_ORDERING
from src.Molecule import Molecule
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.latex.format_irred_representations import format_irred_representations
from src.latex.get_table import get_table


def get_overview_table_for_symmetries(molecule:Molecule, ordering:CI_ORDERING) -> str:
    start = r"\section{Symmetry Conclusion} " + "\n"

    table = ["Dimer State & Symmetry"]
    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule, ordering=ordering)
    symmetries = {}
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()
        table.append(fr"${d.get_label()} \displaystyle $ & ${format_irred_representations(d.symmetry)} \displaystyle $")

        if d.symmetry not in symmetries:
            symmetries[d.symmetry] = 1
        else:
            symmetries[d.symmetry] += 1

    conclusion = "\n\n\n"+ r"$\Rightarrow{}$ "
    conclusion += " and ".join([fr"{count}x ${format_irred_representations(sym)}$" for sym, count in symmetries.items()])
    conclusion += "\n\n"

    return start + get_table(content_lines=table, number_of_columns=2) + conclusion
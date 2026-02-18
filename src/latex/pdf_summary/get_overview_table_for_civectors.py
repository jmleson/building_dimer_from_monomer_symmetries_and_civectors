from src.latex.get_itemize_environment import get_itemize_environment
from src.latex.latex_equation_types import latex_equation_types, get_expression_as_latex_formula
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states


def get_overview_table_for_civectors(molecule:Molecule, ordering:CI_ORDERING) -> str:
    start = "\n" + r"\newpage" + "\n" + r"\section{CI Vector Conclusion} " + "\n"

    start += "Dimer States and Their CI Vectors:"
    main = ""
    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule, ordering=ordering)
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()
        main += r"\item " + rf"\boldmath${d.get_label()} \displaystyle $\unboldmath : \quad"
        main += get_expression_as_latex_formula(d.written_in_dimer_ci_vectors(summed_up=True, short_version=True), latex_equation_types.DISPLAYED)
        main += "\n"

    return start + get_itemize_environment(s=main) + "\n\n"
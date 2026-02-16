from src_alongLaTex.CI_Vectors.get_product_terms import draw
from src_alongLaTex.Molecule import Molecule
from src_alongLaTex.latex.mark_end_of_state import mark_end_of_state
from src_alongLaTex.symmetries.group_theory.PointGroups import POINTGROUP
from src_alongLaTex.symmetries.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from src_alongLaTex.symmetries.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates


def get_linear_combined_states_results(molecule:Molecule, print_ci_vectors:bool, print_symmetries:bool, detailed:bool=False):
    combined_monomer_states = get_monomer_state_linear_combinations(molecule=molecule, detailed=True)[1]

    existing = []
    if print_ci_vectors or print_symmetries:
        content = "\n" + r"\section{Linear Combinations: 16 Monomer- / 8 Dimer-States}" + "\n"
    else:
        content = ""
        detailed = False
    for key, l1 in combined_monomer_states.items():
        monomer_state_1, monomer_state_2 = key.split(" and ")
        combi = sorted([monomer_state_1, monomer_state_2])  # r"beide benötigt; muss sortiert werden, damit Kombination nur 1x vorkommt
        if combi not in existing:
            existing.append(combi)
            if monomer_state_1 == monomer_state_2:
                l1.name = "identical " + l1.name
                content += procedure_single_linear_combination(l=l1, point_group=molecule.get_point_group(),
                                                               print_ci_vectors=print_ci_vectors, print_symmetries=print_symmetries, detailed=detailed)
            else:
                l2 = combined_monomer_states[monomer_state_2 + " and " + monomer_state_1]

                l_plus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_plus.name = "plus combination: " + l1.name + " + " + l2.name + " "
                content += procedure_single_linear_combination(l=l_plus, point_group=molecule.get_point_group(),
                                                               print_ci_vectors=print_ci_vectors,
                                                               print_symmetries=print_symmetries, detailed=detailed)

                l2.change_sign()
                l_minus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_minus.name = "minus combination: " + l1.name + " - " + l2.name + " "
                content += procedure_single_linear_combination(l=l_minus, point_group=molecule.get_point_group(),
                                                               print_ci_vectors=print_ci_vectors,
                                                               print_symmetries=print_symmetries, detailed=detailed)

    return content


def procedure_single_linear_combination(l: linear_combination_of_dimeroccstates, point_group:POINTGROUP,
                                        print_ci_vectors:bool, print_symmetries:bool, detailed:bool):
    content = ""
    # print(l.name)
    if print_ci_vectors:
        content += draw(l, point_group=point_group, detailed=True)
    if print_symmetries:
        if not print_ci_vectors:
            content += l.draw()
        else:
            content += "\n\n" + "or, expressed in terms of symmetry:"
        content += l.build_linear_kombination(detailed=detailed) + " " + "\n\n"
    content += mark_end_of_state()
    # print()
    return content


from CI_Vectors.get_product_terms import draw
from Molecule import Molecule
from latex.mark_end_of_state import mark_end_of_state
from symmetries.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from symmetries.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates


def get_linear_combined_states_results(molecule:Molecule, print_ci_vectors:bool, print_symmetries:bool, detailed:bool=False):
    combined_monomer_states = get_monomer_state_linear_combinations(molecule=molecule, detailed=True)[1]


    existing = []
    if print_ci_vectors ^ print_symmetries:
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
                if print_ci_vectors:
                    l1.name = "identical " + l1.name
                    content += draw(l1, point_group=molecule.get_point_group(), detailed=detailed)
                if print_symmetries:
                    if not print_ci_vectors:
                        content += "identical " + l1.name + r"\\" + "\n"
                        content += l1.draw()
                    else:
                        content += "\n\n" + "or, expressed in terms of symmetry:"
                    content += l1.build_linear_kombination(detailed=detailed) + " "+"\n\n"
                content += mark_end_of_state()
            else:
                l2 = combined_monomer_states[monomer_state_2 + " and " + monomer_state_1]

                l_plus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_plus.name = "plus combination: " + l1.name + " + " + l2.name + " "
                if print_ci_vectors:
                    content += draw(l_plus, point_group=molecule.get_point_group(), detailed=detailed)
                if print_symmetries:
                    if not print_ci_vectors:
                        content += l_plus.draw() + " "
                    else:
                        content += r"\vspace{0.5cm}" + "\n" + "or, expressed in terms of symmetry:"
                    content += l_plus.build_linear_kombination(detailed=detailed) + " "
                content += mark_end_of_state()

                l2.change_sign()
                l_minus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_minus.name = "minus combination: " + l1.name + " - " + l2.name + " "
                if print_ci_vectors:
                    content += draw(l_minus, point_group=molecule.get_point_group(), detailed=detailed)
                if print_symmetries:
                    if not print_ci_vectors:
                        content += l_minus.draw() + " \n "
                    else:
                        content += r"\vspace{0.5cm}" + "\n" + "or, expressed in terms of symmetry:"
                    content += l_plus.build_linear_kombination(detailed=detailed) + " " + "\n\n"
                content += mark_end_of_state()

    return content

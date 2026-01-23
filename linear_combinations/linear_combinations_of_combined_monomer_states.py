# from symmetrie_und_orbitale.get_latex_file_for_all_combinations import get_latex_file_for_d2h_symmetrie_options
from symmetrie_und_orbitale.PointGroups import POINTGROUP
from symmetrie_und_orbitale.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from symmetrie_und_orbitale.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates


def linear_combinations_of_combined_monomer_states(point_group: POINTGROUP, detailed:bool):
    combined_monomer_states = get_monomer_state_linear_combinations(point_group=point_group, detailed=True)[1]

    existing = []
    content = "\n"+r"\section{Linearkombinationen: 16 Monomer- / 8 Dimer-Zustände}"+ "\n"
    for key,l1 in combined_monomer_states.items():
        monomer_state_1, monomer_state_2 = key.split(" und ")

        if monomer_state_1 == monomer_state_2:
            content += "identisch "+ l1.name+ r"\\"+ "\n"
            content += l1.draw()
            content += l1.build_linear_kombination(detailed=detailed) + " "
            content += r"\newpage" + "\n\n"
        else:
            l2 = combined_monomer_states[monomer_state_2+" und "+ monomer_state_1]
            combi = sorted([ l1.name, l2.name])#r"beide benötigt; muss sortiert werden, damit Kombination nur 1x vorkommt
            if combi not in existing:
                print(combi , r"\\\\")
                existing.append(combi)

                l_plus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_plus.name = l1.name+ " + "+ l2.name
                content += "lplus: " + l_plus.name + " "
                content += l_plus.draw()+ " "
                # print(l_plus.draw())
                content += l_plus.build_linear_kombination(detailed=detailed) + " "
                # content += r"\\\\" + "\n"
                if detailed:
                    content += r"\newpage" + "\n\n"

                l2.change_sign()
                l_minus = linear_combination_of_dimeroccstates(l1.dimer_occ_states+l2.dimer_occ_states)
                l_minus.name = l1.name + " - " + l2.name
                content += "lminus: " + l_minus.name + " "
                content += l_minus.draw()+ " \n "
                content += l_plus.build_linear_kombination(detailed=detailed) + " "
                content += "\n\n"

                content += r"\newpage" + "\n\n"

    return content
#
#
# if __name__ == '__name__':
#     # detailed = True
#     detailed = False
#     content = linear_combinations_of_combined_monomer_states(detailed)
#     get_latex_file_for_d2h_symmetrie_options(content)
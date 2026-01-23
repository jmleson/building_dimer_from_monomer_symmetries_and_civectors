from symmetrie_und_orbitale.CI_Vectors.get_product_terms import draw
from symmetrie_und_orbitale.PointGroups import POINTGROUP
from symmetrie_und_orbitale.linear_combinations.linear_combination_monomer_states import \
    get_monomer_state_linear_combinations
from symmetrie_und_orbitale.linear_combinations.linear_combination_of_dimeroccstates import \
    linear_combination_of_dimeroccstates


def get_linear_combined_states(point_group:POINTGROUP):
    combined_monomer_states = get_monomer_state_linear_combinations(point_group=point_group, detailed=True)[1]

    existing = []
    content = "\n" + r"\section{Linearkombinationen: 16 Monomer- / 8 Dimer-Zustände}" + "\n"
    for key, l1 in combined_monomer_states.items():
        monomer_state_1, monomer_state_2 = key.split(" und ")
        combi = sorted([monomer_state_1, monomer_state_2])  # r"beide benötigt; muss sortiert werden, damit Kombination nur 1x vorkommt
        if combi not in existing:
            existing.append(combi)
            if monomer_state_1 == monomer_state_2:
                l1.name = "identisch " + l1.name
                content += draw(l1, point_group=point_group)
            else:
                l2 = combined_monomer_states[monomer_state_2 + " und " + monomer_state_1]

                l_plus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_plus.name = "lplus: " + l1.name + " + " + l2.name + " "
                content += draw(l_plus, point_group=point_group)

                l2.change_sign()
                l_minus = linear_combination_of_dimeroccstates(l1.dimer_occ_states + l2.dimer_occ_states)
                l_minus.name = "lminus: " + l1.name + " - " + l2.name + " "
                content += draw(l_minus, point_group=point_group)

    return content

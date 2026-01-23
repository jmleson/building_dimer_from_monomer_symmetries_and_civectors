from symmetries.group_theory.PointGroups import POINTGROUP
from symmetries.all_products import all_products
from symmetries.linear_combinations.linear_combination_monomer_states import get_monomer_state_linear_combinations
from symmetries.linear_combinations.linear_combinations_of_combined_monomer_states import \
    linear_combinations_of_combined_monomer_states
from symmetries.latex.get_latex_file_for_all_combinations import get_latex_file_for_d2h_symmetry_options


if __name__ == "__main__":
    detailed = True
    # detailed = False
    # point_group = POINTGROUP("c2h")
    # point_group = POINTGROUP("c2v")
    point_group = POINTGROUP("d2h")

    content = all_products(point_group=point_group, monomer_combinations=True, detailed=detailed)
    content += all_products(point_group=point_group,monomer_combinations=False,detailed=detailed)
    content += get_monomer_state_linear_combinations(point_group=point_group,detailed=detailed)[0]
    content += linear_combinations_of_combined_monomer_states(point_group=point_group, detailed=detailed)
    get_latex_file_for_d2h_symmetry_options(content, point_group=point_group)
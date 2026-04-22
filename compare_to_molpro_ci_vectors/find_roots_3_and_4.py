import copy
import re


from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule



dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6, ordering=CI_ORDERING.molpro)


special_states = []
for d in dimer_states:
    if d.monomer_state_1.label != d.monomer_state_2.label:
        continue
    if not "e" in d.monomer_state_1.label:
        continue

    d.get_product_terms()
    d.get_determinants()
    d.sum_up_determinants()


    ci_vectors = [i.latex_ci_equation(short_version=True) for i in d.summed_up_list_of_determinants_ci]
    simplified_ci_vectors = [
            ('+' if '+' in i else '-') + re.search(r'\\left\|(.*?)\\right\|', i).group(1)
            for i in ci_vectors
    ]
    print(d.get_label(), simplified_ci_vectors)
    special_states.append(d)



print()
if len(special_states) == 2:
    # positive LC:
    d1, d2 = copy.deepcopy(special_states[0]), copy.deepcopy(special_states[1])
    d1.full_list_of_determinants.extend(d2.full_list_of_determinants)
    d1.sum_up_determinants()
    ci_vectors = [i.latex_ci_equation(short_version=True) for i in d2.summed_up_list_of_determinants_ci]
    simplified_ci_vectors = [
            ('+' if '+' in i else '-') + re.search(r'\\left\|(.*?)\\right\|', i).group(1)
            for i in ci_vectors
    ]
    print(d1.get_label() + " + "+ d2.get_label(), simplified_ci_vectors)

    # # negative LC:
    # d1, d2 = copy.deepcopy(special_states[0]), copy.deepcopy(special_states[1])
    # for i in d2.full_list_of_determinants:
    #     i.sign = SIGN.PLUS if i.sign == SIGN.MINUS else SIGN.MINUS
    # d1.full_list_of_determinants.extend(d2.full_list_of_determinants)
    # d1.sum_up_determinants()
    # ci_vectors = [i.latex_ci_equation(short_version=True) for i in d2.summed_up_list_of_determinants_ci]
    # simplified_ci_vectors = [
    #     ('+' if '+' in i else '-') + re.search(r'\\left\|(.*?)\\right\|', i).group(1)
    #     for i in ci_vectors
    # ]
    # print(d1.get_label() + " - " + d2.get_label(), simplified_ci_vectors)


# ########
# print("\nin Molpro it is: ")
# path = f"compare_to_molpro_ci_vectors/data_storage/"
# file = f"C6H6-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ200-Plots.out"
# info = parse_output_file_for_state_dependent_ci_vectors(path + file)
#
# print("state 4.1 = ", end="\t")
# for key, value in info["4.1"].items():
#     value = value if "-" in value else "+"+value
#     print(value , "*" , key.replace(" ",""), end="\t")
# print()
#
# print("state 5.1 = ", end="\t")
# for key, value in info["5.1"].items():
#     value = value if "-" in value else "+"+value
#     print(value , "*" , key.replace(" ",""), end="\t")
# print()

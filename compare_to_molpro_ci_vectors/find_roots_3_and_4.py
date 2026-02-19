import re


from get_molpro_state_from_molpro_output import get_molpro_state_from_molpro_output
from src.building_blocks.DimerState import DimerState


def flip_sign_variants(variants: list[str]) -> list[str]:
    flipped = []
    for v in variants:
        if v.startswith("+"):
            flipped.append("-" + v[1:])
        elif v.startswith("-"):
            flipped.append("+" + v[1:])
        else:
            raise ValueError(f"Variant has no leading sign: {v}")
    return flipped

def find_dimer_state_by_molpro_variants(data:str, dimer_states:list[DimerState], row_index:int):
    variants_according_to_molpro = get_molpro_state_from_molpro_output(data, row_index)

    fitting_dimer_states = []
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()
        if check_if_dimer_state_fits_molpro_results(dimer_state=d, variants_according_to_molpro=variants_according_to_molpro):
            fitting_dimer_states.append(d)
    return fitting_dimer_states



def check_if_dimer_state_fits_molpro_results(dimer_state:DimerState, variants_according_to_molpro:list[str]):
    ci_vectors = [i.latex_ci_equation(short_version=True) for i in dimer_state.summed_up_list_of_determinants_ci]
    simplified_ci_vectors = [
            ('+' if '+' in i else '-') + re.search(r'\\left\|(.*?)\\right\|', i).group(1)
            for i in ci_vectors
    ]

    sign_switched_variants = flip_sign_variants(variants_according_to_molpro)
    all_molpro = all(v in simplified_ci_vectors for v in variants_according_to_molpro)
    all_sign_switched = all(v in simplified_ci_vectors for v in sign_switched_variants)
    if all_molpro or all_sign_switched:
        return True
    else:
        return False




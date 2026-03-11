import re


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
        return True, ""
    else:
        all_molpro = [v in simplified_ci_vectors for v in variants_according_to_molpro]
        all_sign_switched = [v in simplified_ci_vectors for v in sign_switched_variants]
        max_found = max(len(all_molpro), len(all_sign_switched))
        if len(variants_according_to_molpro) > len(simplified_ci_vectors):
            info = f"{dimer_state.get_label()}: more states in Molpro"
        elif len(variants_according_to_molpro) < len(simplified_ci_vectors):
            info = f"{dimer_state.get_label()}: less states in Molpro"
        else:
            if max_found == len(variants_according_to_molpro):
                info = f"{dimer_state.get_label()}: ci vectors fitting, but signs are differing"
            else:
                info = f"{dimer_state.get_label()}: ci vectors unfitting"
        return False, info




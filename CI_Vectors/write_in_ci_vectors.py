from fractions import Fraction

from CI_Vectors.get_possible_dimer_ci import get_possible_dimer_ci
from symmetries.dimer_occ_state import dimer_occ_state
from symmetries.general_functionalities.monomer_positions import MonomerPositions
from symmetries.linear_combinations import \
    linear_combination_of_dimeroccstates


def write_in_ci_vectors(l:linear_combination_of_dimeroccstates):
    content = "\nbzw. in CI-Vektoren geschrieben: \n $$"
    dimer_ci_vectors = []
    counter = 0
    for summand in l.dimer_occ_states:
        # print("summand", summand, type(summand))
        content_tmp, dimer_ci_vectors_tmp = dimer_summand_to_dimer(summand=summand)
        dimer_ci_vectors += dimer_ci_vectors_tmp
        if counter >= 5:
            content += " $$ $$ "
        counter += 1
        counter %= 6
        content += content_tmp

    content += "$$\n\n"  # Monomer-Ci-Vektoren ergänzt
    return content, dimer_ci_vectors


def dimer_summand_to_dimer(summand:dimer_occ_state):
    dimer_ci_vectors = []
    content = ""
    # print("dimer_summand_to_dimer", summand, type(summand))
    summand.occupied_mos.keys()
    ci_vector_left = "".join(
        str(summand.occupied_mos[irrep][MonomerPositions.left])
        for irrep in summand.point_group.choices_irreduzible_representations_molpro_ordered
        if irrep in summand.occupied_mos
    )
    ci_vector_right = "".join(
        str(summand.occupied_mos[irrep][MonomerPositions.right])
        for irrep in summand.point_group.choices_irreduzible_representations_molpro_ordered
        if irrep in summand.occupied_mos
    )

    ci_vector_right = ci_vector_right.replace("1", "a").replace(" ", "0")
    ci_vector_left = ci_vector_left.replace("1", "a").replace(" ", "0")

    factor = summand.sign_and_factor
    if factor == 0:
        return content, dimer_ci_vectors
    elif factor < 0:
        sign = "-"
        factor = abs(factor)
    else:
        sign = "+"
    content += (fr"{sign} {factor} \cdot " + r"\left|" + f"{ci_vector_left} " + r"\right|"
                + r" \cdot " + r"\left|" f" {ci_vector_right} " + r"\right|" + " \n")

    counted_dimer_possibilities = get_possible_dimer_ci(ci_vector_left, ci_vector_right)
    number_total = sum([c["count"] for c in counted_dimer_possibilities])

    for ci in counted_dimer_possibilities:
        factor = Fraction(summand.sign_and_factor, number_total) * ci["count"]
        item = {"factor": factor, "sequence": ci["sequence"]}
        dimer_ci_vectors.append(item)
    return content, dimer_ci_vectors
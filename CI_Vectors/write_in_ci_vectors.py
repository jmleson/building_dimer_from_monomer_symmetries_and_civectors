from fractions import Fraction

from CI_Vectors.get_possible_dimer_ci import get_possible_dimer_ci
from dimer_occ_state import dimer_occ_state
from linear_combinations.linear_combination_of_dimeroccstates import \
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
    # molpro order: Ag + B3u + B2u + B1g   +   B1u + B2g + B3g + Au
    ci_vector_left = (f'{summand.occupied_mos["b1u"]["left"]}{summand.occupied_mos["b2g"]["left"]}'
                      + f'{summand.occupied_mos["b3g"]["left"]}{summand.occupied_mos["au"]["left"]}')
    ci_vector_right = (f'{summand.occupied_mos["b1u"]["right"]}{summand.occupied_mos["b2g"]["right"]}'
                       + f'{summand.occupied_mos["b3g"]["right"]}{summand.occupied_mos["au"]["right"]}')

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
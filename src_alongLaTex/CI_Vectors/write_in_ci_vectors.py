from fractions import Fraction

from src_alongLaTex.CI_Vectors.get_possible_dimer_ci import get_possible_dimer_ci
from src_alongLaTex.symmetries.dimer_occ_state import dimer_occ_state
from src_alongLaTex.symmetries.general_functionalities.monomer_positions import MonomerPositions
from src_alongLaTex.symmetries.group_theory.PointGroups import POINTGROUP
from src_alongLaTex.symmetries.linear_combinations import linear_combination_of_dimeroccstates


def write_in_ci_vectors(l: linear_combination_of_dimeroccstates, break_after_number_of_terms:int=5):
    content = "\nwritten in CI Vectors: \n $$"
    dimer_ci_vectors = []
    counter = 0
    for summand in l.dimer_occ_states:
        # print("summand", summand, type(summand))
        content_tmp, dimer_ci_vectors_tmp = dimer_summand_to_dimer(summand=summand)
        dimer_ci_vectors += dimer_ci_vectors_tmp
        if counter >= break_after_number_of_terms:
            content += " $$ $$ "
        counter += 1
        counter %= break_after_number_of_terms+1
        content += content_tmp

    content += "$$\n\n"  # Monomer-Ci-Vektoren ergänzt
    return content, dimer_ci_vectors



def occupied_mos_to_ci(occupied_mos:dict, monomerposition:MonomerPositions, point_group:POINTGROUP):
    ci_vector = "".join(
        str(occupied_mos[irrep][monomerposition])
        for irrep in point_group.choices_irreduzible_representations_molpro_ordered
        if irrep in occupied_mos.keys()
    )
    ci_vector = ci_vector.replace("1", "a").replace(" ", "0")
    return ci_vector

def dimer_summand_to_dimer(summand:dimer_occ_state):
    dimer_ci_vectors = []
    content = ""
    # print("dimer_summand_to_dimer", summand, type(summand))
    # summand.occupied_mos.keys()
    ci_vector_left = occupied_mos_to_ci(occupied_mos=summand.occupied_mos, monomerposition=MonomerPositions.left,
                                        point_group=summand.point_group)
    ci_vector_right = occupied_mos_to_ci(occupied_mos=summand.occupied_mos, monomerposition=MonomerPositions.right,
                                         point_group=summand.point_group)

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
    number_total = sum([abs(c["count"]) for c in counted_dimer_possibilities])

    for ci in counted_dimer_possibilities:
        if number_total == 0:
            factor = 0
        else:
            factor = Fraction(summand.sign_and_factor, number_total) * ci["count"]
        item = {"factor": factor, "sequence": ci["sequence"]}
        dimer_ci_vectors.append(item)
    return content, dimer_ci_vectors

from fractions import Fraction

from CI_Vectors.count import combine_sequences
from CI_Vectors.write_in_ci_vectors import write_in_ci_vectors
from symmetries.Molecule import Molecule
from symmetries.linear_combinations import \
    linear_combination_of_dimeroccstates
from symmetries.group_theory.PointGroups import POINTGROUP
from symmetries.linear_combinations.linear_combination_monomer_states import get_monomer_combinations, \
    get_linear_combination_of_dimeroccstates_from_combinations


def fraction_to_tex(frac: Fraction) -> str:
    if frac.denominator == 1:
        return str(frac.numerator)  # ganze Zahl
    return fr"\frac{{{frac.numerator}}}{{{frac.denominator}}}"






def draw(l:linear_combination_of_dimeroccstates, point_group: POINTGROUP):
    content = "\n\n" + r"\begin{minipage}{\linewidth}" + "\n"

    l.name = l.name.replace("and", "*")
    content += l.name
    if point_group == POINTGROUP.D2h:# FALL C6H6 !!! TODO
        content += r" \quad = \quad "
        name = (l.name.replace("i^3 b_{2u}", "1.3").replace("i^3 b_{3u}", "2.2")
                .replace("e^3 b_{2u}", "2.3").replace("e^3 b_{3u}", "1.2"))
        content += name + "\n"

    content += l.draw() + "\n\n"
    content_tmp, dimer_ci_vectors = write_in_ci_vectors(l=l)
    content += content_tmp

    content += dimer_ci_vectors_to_added_up_sequence(dimer_ci_vectors=dimer_ci_vectors)

    content += "\n\n" + r"\end{minipage}" + "\n" + r"\vspace{0.5cm}" + "\n" + r"\hrule" + "\n" + r"\vspace{0.5cm}" + "\n\n"
    return content

def get_product_terms(molecule:Molecule):
    content = r"\section{Multiplications}" + "\n"
    combinations = get_monomer_combinations(molecule=molecule)

    for combination in combinations:
        # content += "\n\n" + r"\begin{minipage}{\linewidth}" + "\n"
        # state_1 = combination[0].name
        # state_2 = combination[1].name
        # molpro_1 = state_1.replace("i^3 b_{2u}", "1.3").replace("i^3 b_{3u}", "2.2").replace("e^3 b_{2u}", "2.3").replace("e^3 b_{3u}", "1.2")
        # molpro_2 = state_2.replace("i^3 b_{2u}", "1.3").replace("i^3 b_{3u}", "2.2").replace("e^3 b_{2u}", "2.3").replace("e^3 b_{3u}", "1.2")
        # content += state_1 + " * " + state_2 + r" \quad = \quad " + molpro_1 + " * " + molpro_2 + ":\n\n"
        # split monomers-occupations:
        l = get_linear_combination_of_dimeroccstates_from_combinations(combination=combination, molecule=molecule)
        # print(l.name)
        content += draw(l=l, point_group=molecule.get_point_group() )
        # content += "\n\n" + r"\end{minipage}" + "\n" + r"\vspace{0.5cm}" + "\n" + r"\hrule" + "\n" + r"\vspace{0.5cm}" + "\n\n"

    return content

def dimer_ci_vectors_to_added_up_sequence(dimer_ci_vectors:list):
    content = ""
    dimer_ci_vectors = combine_sequences(data=dimer_ci_vectors)
    # add dimer-CI-vectors:
    content += "\n\n bildet folgende mögliche Dimerkombinationen:\n"
    counter = 0
    content += "\n$$"  # ! needed, s. if below
    for i in dimer_ci_vectors:
        factor = i['factor']
        if factor == 0:
            continue
        elif factor < 0:
            sign = "-"
            factor = abs(factor)
        else:
            sign = "+"
        if counter == 0 or counter >= 6:
            if content[-2:] != "$$":  # stop at start of adding
                content += " $$ $$ "
        counter += 1
        counter %= 6

        content += fr"{sign} {fraction_to_tex(factor)} \cdot " + r"\left|" + f"{i['sequence']} " + r"\right| "
    content += "$$\n\n"
    return content



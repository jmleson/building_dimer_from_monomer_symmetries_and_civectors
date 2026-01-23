import itertools
from typing import Tuple, List

from symmetries.PointGroups import POINTGROUP
from symmetries.dimer_occ_state import dimer_occ_state
from symmetries.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates
from symmetries.switch_monomers import switch_monomers



def get_possible_occs() -> List[Tuple]:
    """
    calculates all possible states with 4 electrons in 4 orbitals, where:
        amount of electrons in binding orbitals >= number of electrons in upper two orbitls
    <-> singlett, quintett, and 4 triplett states
    :return: list of 4 tuples containing the occupation numbers of different states
    """
    values = [0, 1, 2]
    combinations = itertools.product(values, repeat=4)
    valid_combinations = [comb for comb in combinations if sum(comb) == 4 and (
            (comb[0] + comb[1]) > (comb[2] + comb[3]) or (comb[0] == 1 and comb[1] == 1 and comb[2] == 1 and comb[3] == 1)
    ) ]
    return valid_combinations



def all_products(point_group:POINTGROUP, monomer_combinations:bool=True, detailed:bool=True) -> str:
    """
    calculating all linear combinations of 2 monomer states or 4 monomer states
    :param monomer_combinations: toggle between calculating all
            monomer combinations (true)
            or linear combinations of the monomer combinations (false)
    :param detailed: give detailed formulas (true) or just give the compact form (false)
    :return: latex formatted result
    """
    if monomer_combinations:
        content = r"\newpage \section{Linearkombinationen: 2 Monomer- / 1 Dimer-Zustände}"+"\n"
    else:
        content = r"\newpage \section{Linearkombinationen: 4 Monomer- / 2 Dimer-Zustände}"+"\n"
    valid_combinations = get_possible_occs()
    for i in range(len(valid_combinations)):
        monomer_a = valid_combinations[i]
        for j in range(i, len(valid_combinations)):
            monomer_b = valid_combinations[j]
            number_unpaired = monomer_a.count(1) + monomer_b.count(1)
            if number_unpaired == 4:
                if point_group == POINTGROUP.D2h:
                    occupied_mos = {
                        "b1u": {"left": monomer_a[2], "right": monomer_b[2]},#antibindend
                        "au":  {"left": monomer_a[3], "right": monomer_b[3]},#antibindend
                        "b2g": {"left": monomer_a[0], "right": monomer_b[0]},# bindend (erste OCC)
                        "b3g": {"left": monomer_a[1], "right": monomer_b[1]},# bindend (erste OCC)
                    }
                    print("occupied mos", occupied_mos)
                else:# C2v und C2h
                    occupied_mos = {
                        "b2*": {"left": monomer_a[2], "right": monomer_b[2]},  # antibindend
                        "a2*": {"left": monomer_a[3], "right": monomer_b[3]},  # antibindend
                        "a2": {"left": monomer_a[0], "right": monomer_b[0]},  # bindend (erste OCC)
                        "b2": {"left": monomer_a[1], "right": monomer_b[1]},  # bindend (erste OCC)
                    }
                d = dimer_occ_state(occupied_mos=occupied_mos,point_group=point_group)
                d2 = dimer_occ_state(occupied_mos=switch_monomers(occupied_mos),point_group=point_group)
                ##### CASES ####
                if monomer_combinations:
                    content += d.print(detailed)
                    if i != j:
                        content += "\n"+r"\vspace{0.5cm}"+"\n"
                        content += d2.print(detailed)
                    # content = #r"\\",
                    content +="\n"+ r"\hrule\newpage "+ "\n\n"
                else:
                    l = linear_combination_of_dimeroccstates([d, d2])
                    content += l.draw()
                    content += l.get_info_about_involved_monomer_symmetries()
                    content += l.build_linear_kombination(detailed)
                    l.change_combination()
                    if l.check_valitity():
                        content += "\n" + r"\vspace{0.5cm}" + "\n"
                        content += l.draw()
                        content += l.get_info_about_involved_monomer_symmetries()
                        content += l.build_linear_kombination(detailed)
                    content += "\n"+r"\hrule\newpage "+ "\n"#\vspace{0.5cm}
    return content




if __name__ == '__main__':
    all_products(True)
    # all_products(False)
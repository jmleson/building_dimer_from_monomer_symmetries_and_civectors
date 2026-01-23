import itertools
from typing import Tuple, Dict

from symmetrie_und_orbitale.PointGroups import POINTGROUP
from symmetrie_und_orbitale.dimer_occ_state import dimer_occ_state
from symmetrie_und_orbitale.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates
from symmetrie_und_orbitale.linear_combinations.monomer_state import monomer_state



def get_monomer_combinations(point_group: POINTGROUP):
    # Vorgabe:
    occupied_mos = {
        point_group.label["oben_links"]: {"left": 1, "right": 0},  # b1u
        point_group.label["oben_rechts"]: {"left": 0, "right": 1},  # "au"
        point_group.label["unten_links"]: {"left": 2, "right": 1},  # "b2g"
        point_group.label["unten_rechts"]: {"left": 1, "right": 2},  # "b3g"
    }
    if point_group == POINTGROUP.D2h:
        m1 = monomer_state(occupied_mos, "$i^3 b_{2u}$", "-")
        m2 = monomer_state(occupied_mos, "$e^3 b_{2u}$", "+")
    elif point_group == POINTGROUP.C2v or point_group == POINTGROUP.C2h:
        m1 = monomer_state(occupied_mos, "$i^3 a_1$", "-")
        m2 = monomer_state(occupied_mos, "$e^3 a_1$", "+")
    else:
        raise Exception("not yet implemented")
    occupied_mos = {
        point_group.label["oben_links"]: {"left": 1, "right": 0},
        point_group.label["oben_rechts"]: {"left": 0, "right": 1},
        point_group.label["unten_links"]: {"left": 1, "right": 2},
        point_group.label["unten_rechts"]: {"left": 2, "right": 1},
    }
    if point_group == POINTGROUP.D2h:
        m3 = monomer_state(occupied_mos, "$e^3 b_{3u}$", "-")
        m4 = monomer_state(occupied_mos, "$i^3 b_{3u}$", "+")
    elif point_group == point_group.C2v or point_group == POINTGROUP.C2h:
        m3 = monomer_state(occupied_mos, "$e^3 b_{1}$", "-")
        m4 = monomer_state(occupied_mos, "$i^3 b_{1}$", "+")
    else:
        raise Exception("error again")  # Fehler sollte oben schon geworfen werden, wenn unbekannte Punktgruppe

    monomers = [m1, m2, m3, m4]
    return list(itertools.product(monomers, repeat=2))



def get_linear_combination_of_dimeroccstates_from_combinations(combination, point_group:POINTGROUP):
    # split monomers-occupations:
    left1_occ = {key: value["left"] for key, value in combination[0].occupied_mos.items()}
    right1_occ = {key: value["right"] for key, value in combination[0].occupied_mos.items()}
    left2_occ = {key: value["left"] for key, value in combination[1].occupied_mos.items()}
    right2_occ = {key: value["right"] for key, value in combination[1].occupied_mos.items()}

    # multiply occupied_mos:
    ''' left * right
    Fall 1:     (l1+r1)*(l2+r2) = l1*l2 + r1*l2 + l1*r2 + r1*r2
    Fall 2:     (l1-r1)*(l2-r2) = l1*l2 - r1*l2 - l1*r2 + r1*r2
    Fall 3:     (l1+r1)*(l2-r2) = l1*l2 + r1*l2 - l1*r2 - r1*r2
    Fall 4:     (l1-r1)*(l2+r2) = l1*l2 - r1*l2 + l1*r2 - r1*r2
    '''
    # combine monomer occupations:
    reconstructed_dict_term1 = {key: {"left": left1_occ[key], "right": left2_occ[key]} for key in left1_occ}  # immer +
    d1 = dimer_occ_state(occupied_mos=reconstructed_dict_term1, sign_and_factor=+1, point_group=point_group)

    reconstructed_dict_term2 = {key: {"left": right1_occ[key], "right": left2_occ[key]} for key in left1_occ}
    sign = -1 if combination[0].initial_kombination == "-" else +1
    d2 = dimer_occ_state(occupied_mos=reconstructed_dict_term2, sign_and_factor=sign, point_group=point_group)

    reconstructed_dict_term3 = {key: {"left": left1_occ[key], "right": right2_occ[key]} for key in left1_occ}
    sign = -1 if combination[1].initial_kombination == "-" else +1
    d3 = dimer_occ_state(occupied_mos=reconstructed_dict_term3, sign_and_factor=sign, point_group=point_group)

    reconstructed_dict_term4 = {key: {"left": right1_occ[key], "right": right2_occ[key]} for key in left1_occ}
    sign = +1 if combination[0].initial_kombination == combination[1].initial_kombination else -1
    d4 = dimer_occ_state(occupied_mos=reconstructed_dict_term4, sign_and_factor=sign, point_group=point_group)

    l = linear_combination_of_dimeroccstates([d1, d2, d3, d4])
    name = combination[0].name + " und " + combination[1].name
    l.name = name
    return l


def get_monomer_state_linear_combinations(point_group: POINTGROUP, detailed:bool=True)-> Tuple[ str, Dict ]:
    # if point_group != POINTGROUP.D2h:
    #     raise Exception("nyi")
    combined_monomer_states = {} # Sammeln der ausgedruckten Kombinationen von Monomerzuständen (damit daraus noch wieder Linearkombinationen gebildet werden können)
    # # Vorgabe:
    # occupied_mos = {
    #     point_group.label["oben_links"]: {"left": 1, "right": 0},# b1u
    #     point_group.label["oben_rechts"]:  {"left": 0, "right": 1},#"au"
    #     point_group.label["unten_links"]: {"left": 2, "right": 1},#"b2g"
    #     point_group.label["unten_rechts"]: {"left": 1, "right": 2},#"b3g"
    # }
    # if point_group == POINTGROUP.D2h:
    #     m1 = monomer_state(occupied_mos, "$i^3 b_{2u}$", "-")
    #     m2 = monomer_state(occupied_mos, "$e^3 b_{2u}$", "+")
    # elif point_group == POINTGROUP.C2v or point_group == POINTGROUP.C2h:
    #     m1 = monomer_state(occupied_mos, "$i^3 a_1$", "-")
    #     m2 = monomer_state(occupied_mos, "$e^3 a_1$", "+")
    # else:
    #     raise Exception("not yet implemented")
    # occupied_mos = {
    #     point_group.label["oben_links"]: {"left": 1, "right": 0},
    #     point_group.label["oben_rechts"]: {"left": 0, "right": 1},
    #     point_group.label["unten_links"]: {"left": 1, "right": 2},
    #     point_group.label["unten_rechts"]: {"left": 2, "right": 1},
    # }
    # if point_group == POINTGROUP.D2h:
    #     m3 = monomer_state(occupied_mos, "$e^3 b_{3u}$", "-")
    #     m4 = monomer_state(occupied_mos, "$i^3 b_{3u}$", "+")
    # elif point_group == point_group.C2v or point_group == POINTGROUP.C2h:
    #     m3 = monomer_state(occupied_mos, "$e^3 b_{1}$", "-")
    #     m4 = monomer_state(occupied_mos, "$i^3 b_{1}$", "+")
    # else:
    #     raise Exception("error again")# Fehler sollte oben schon geworfen werden, wenn unbekannte Punktgruppe
    #
    # monomers=[m1,m2,m3,m4]
    # kombinationen = list(itertools.product(monomers, repeat=2))
    kombinationen = get_monomer_combinations(point_group=point_group)

    content = "\n"+r"\section{Linearkombinationen: 8 Monomer- / 4 Dimer-Zustände}"+"\n"
    pagebreak = True
    for combination in kombinationen:
        pagebreak = not pagebreak
        content += combination[0].name+ " * "+ combination[1].name+ ":\n\n"

        l = get_linear_combination_of_dimeroccstates_from_combinations(combination=combination, point_group=point_group)
        combined_monomer_states[l.name] = l

        content += l.draw()+"\n"
        content += l.build_linear_kombination(detailed=detailed)+"\n"
        if pagebreak:
            content += r"\newpage"+"\n\n"
        else:
            content += r"\vspace{1cm}"+"\n\n"
    return content, combined_monomer_states




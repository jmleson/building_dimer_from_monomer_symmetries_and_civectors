import itertools
from typing import Tuple, Dict

from src_alongLaTex.Molecule import Molecule
from src_alongLaTex.symmetries.dimer_occ_state import dimer_occ_state
from src_alongLaTex.symmetries.general_functionalities.monomer_positions import MonomerPositions
from src_alongLaTex.symmetries.linear_combinations.linear_combination_of_dimeroccstates import linear_combination_of_dimeroccstates
from src_alongLaTex.symmetries.linear_combinations.monomer_state import monomer_state



def get_monomer_combinations(molecule: Molecule):
    m_state_info = molecule.get_ci_vectors_triplets()
    #INFO: INPUT according to CI-Vectors of triplet calculation:

    monomers = []
    for sym_infos in m_state_info:
        for name, initial_combination in sym_infos["included states"]:
            m = monomer_state(sym_infos["occupied_mos"], name=name, initial_combination=initial_combination)
            monomers.append(m)

    return list(itertools.product(monomers, repeat=2))



def get_linear_combination_of_dimeroccstates_from_combinations(combination, molecule:Molecule):
    point_group = molecule.get_point_group()
    # split monomers-occupations:
    left1_occ = {key: value[MonomerPositions.left] for key, value in combination[0].occupied_mos.items()}
    right1_occ = {key: value[MonomerPositions.right] for key, value in combination[0].occupied_mos.items()}
    left2_occ = {key: value[MonomerPositions.left] for key, value in combination[1].occupied_mos.items()}
    right2_occ = {key: value[MonomerPositions.right] for key, value in combination[1].occupied_mos.items()}

    # multiply occupied_mos:
    ''' left * right
    Fall 1:     (l1+r1)*(l2+r2) = l1*l2 + r1*l2 + l1*r2 + r1*r2
    Fall 2:     (l1-r1)*(l2-r2) = l1*l2 - r1*l2 - l1*r2 + r1*r2
    Fall 3:     (l1+r1)*(l2-r2) = l1*l2 + r1*l2 - l1*r2 - r1*r2
    Fall 4:     (l1-r1)*(l2+r2) = l1*l2 - r1*l2 + l1*r2 - r1*r2
    '''
    # combine monomer occupations:
    reconstructed_dict_term1 = {key: {MonomerPositions.left: left1_occ[key], MonomerPositions.right: left2_occ[key]} for key in left1_occ}  # immer +
    d1 = dimer_occ_state(occupied_mos=reconstructed_dict_term1, sign_and_factor=+1, point_group=point_group)

    reconstructed_dict_term2 = {key: {MonomerPositions.left: right1_occ[key], MonomerPositions.right: left2_occ[key]} for key in left1_occ}
    sign = -1 if combination[0].initial_kombination == "-" else +1
    d2 = dimer_occ_state(occupied_mos=reconstructed_dict_term2, sign_and_factor=sign, point_group=point_group)

    reconstructed_dict_term3 = {key: {MonomerPositions.left: left1_occ[key], MonomerPositions.right: right2_occ[key]} for key in left1_occ}
    sign = -1 if combination[1].initial_kombination == "-" else +1
    d3 = dimer_occ_state(occupied_mos=reconstructed_dict_term3, sign_and_factor=sign, point_group=point_group)

    reconstructed_dict_term4 = {key: {MonomerPositions.left: right1_occ[key], MonomerPositions.right: right2_occ[key]} for key in left1_occ}
    sign = +1 if combination[0].initial_kombination == combination[1].initial_kombination else -1
    d4 = dimer_occ_state(occupied_mos=reconstructed_dict_term4, sign_and_factor=sign, point_group=point_group)

    l = linear_combination_of_dimeroccstates([d1, d2, d3, d4])
    name = combination[0].name + " and " + combination[1].name
    l.name = name
    return l


def get_monomer_state_linear_combinations(molecule:Molecule, detailed:bool=True)-> Tuple[ str, Dict ]:
    combined_monomer_states = {} # Sammeln der ausgedruckten Kombinationen von Monomerzuständen (damit daraus noch wieder Linear Combinations gebildet werden können)
    kombinationen = get_monomer_combinations(molecule=molecule)

    content = "\n"+r"\section{Linear Combinations: 8 Monomer- / 4 Dimer-States}"+"\n"
    pagebreak = True
    for combination in kombinationen:
        pagebreak = not pagebreak
        content += combination[0].name+ " * "+ combination[1].name+ ":\n\n"

        l = get_linear_combination_of_dimeroccstates_from_combinations(combination=combination, molecule=molecule)
        combined_monomer_states[l.name] = l

        content += l.draw()+"\n"
        content += l.build_linear_kombination(detailed=detailed) + "\n"
        if pagebreak:
            content += r"\newpage"+"\n\n"
        else:
            content += r"\vspace{1cm}"+"\n\n"
    return content, combined_monomer_states




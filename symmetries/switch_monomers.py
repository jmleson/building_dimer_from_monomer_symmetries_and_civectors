import copy
from typing import Dict

from symmetries.general_functionalities.monomer_positions import MonomerPositions


def switch_monomers(occupied_mos:Dict) -> Dict :
    """
    exchanging the monomer occupations within a dictionary of left / right monomer occupations
    :param occupied_mos: occupied mos given by symmetry label and MonomerPositions.left/MonomerPositions.right for the choice of monomer
    :return: occupied_mos with monomers exchanged
    """
    new = copy.deepcopy(occupied_mos)
    for key, value in new.items():
        value[MonomerPositions.left], value[MonomerPositions.right] = value[MonomerPositions.right], value[MonomerPositions.left]
    return new


if __name__ == '__main__':
    occupied_mos = {
        "b1u": {MonomerPositions.left: 0, MonomerPositions.right: 1},
        "au": {MonomerPositions.left: 0, MonomerPositions.right: 1},
        "b2g": {MonomerPositions.left: 2, MonomerPositions.right: 1},
        "b3g": {MonomerPositions.left: 2, MonomerPositions.right: 1},
    }
    print(switch_monomers(occupied_mos))

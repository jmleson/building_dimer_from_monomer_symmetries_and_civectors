import copy
from typing import Dict


def switch_monomers(occupied_mos:Dict) -> Dict :
    """
    exchanging the monomer occupations within a dictionary of left / right monomer occupations
    :param occupied_mos: occupied mos given by symmetry label and "left"/"right" for the choice of monomer
    :return: occupied_mos with monomers exchanged
    """
    new = copy.deepcopy(occupied_mos)
    for key, value in new.items():
        value["left"], value["right"] = value["right"], value["left"]
    return new


if __name__ == '__main__':
    occupied_mos = {
        "b1u": {"left": 0, "right": 1},
        "au": {"left": 0, "right": 1},
        "b2g": {"left": 2, "right": 1},
        "b3g": {"left": 2, "right": 1},
    }
    print(switch_monomers(occupied_mos))

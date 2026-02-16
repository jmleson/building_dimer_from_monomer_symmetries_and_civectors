
from enum import Enum

class term_step(Enum):
    """
    different options for the list of determinants of the monomer/dimer states;
    offering uniform string descriptions, to avoid errors due to typos
    """
    COMBINED = "combined"
    SORTED = "combined and sorted"
    EVALUATED = "combined, sorted and duplicates removed"




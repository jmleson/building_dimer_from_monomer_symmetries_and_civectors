from src_alongLaTex.CI_Vectors.write_in_ci_vectors import occupied_mos_to_ci
from src_alongLaTex.Molecule import Molecule
from src_alongLaTex.get_mo_schema import get_mo_schemata, wrap_tikzpicture
from src_alongLaTex.symmetries.general_functionalities.monomer_positions import MonomerPositions


def get_monomer_states_and_configurations(molecule:Molecule):
    start = r"\section{Monomer States and Configurations} "  + "\n"
    point_group = molecule.get_point_group()

    # CASCI-Information about Monomer-CI's:
    triplet_states = molecule.get_ci_vectors_triplets()
    for triplet_sym in triplet_states:
        mos = triplet_sym["occupied_mos"]
        monomer_orbitals_left = get_mo_schemata(occupied_mos=mos, monomer=MonomerPositions.left, point_group=point_group)
        monomer_orbitals_right = get_mo_schemata(occupied_mos=mos, monomer=MonomerPositions.right, point_group=point_group)
        for state, add_sign in triplet_sym["included states"]:
            start += "\n" + r"\[" + state.replace("$","") + "\n"
            start += ( r"\quad = + \left(" + wrap_tikzpicture(monomer_orbitals_left) # <- always positive on left hand side
                      + r"\right)" + add_sign + r"\left(" + wrap_tikzpicture(monomer_orbitals_right)
                       + r"\right) \qquad"
                      )

            ci_vector_left = occupied_mos_to_ci(occupied_mos = mos, point_group=point_group,
                                                monomerposition=MonomerPositions.left)
            ci_vector_right = occupied_mos_to_ci(occupied_mos=mos, point_group=point_group,
                                                monomerposition=MonomerPositions.right)
            start += r" = \left|" + ci_vector_left + r"\right|" + add_sign + r"\left|"+ ci_vector_right + r"\right| \]"

            start += "\n\n\n"

    return start + r"\newpage" + "\n\n"
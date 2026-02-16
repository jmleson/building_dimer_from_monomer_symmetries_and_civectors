from enum import Enum

from src.MonomerOccupation import MonomerOccupation
from src.MonomerState import MonomerState
from src.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class Molecule(Enum):
    C6H6 = "Benzene"
    C6H5Cl = "Chlorobenzene"
    C6H5Cl_rotated = "Chlorobenzene (rotated)"

    def get_point_group(self):
        if self.value == Molecule.C6H6.value:
            return POINTGROUP.D2h
        if self.value == Molecule.C6H5Cl.value:
            return POINTGROUP.C2v
        if self.value == Molecule.C6H5Cl_rotated.value:
            return POINTGROUP.C2h
        else:
            raise Exception("unknown how to handle molecule")

    def get_info_file(self):
        if self.value == Molecule.C6H6.value:
            return "DimerZOrbitalordnung-gesamt-MO-C6H6-beiWW.pdf"
        if self.value == Molecule.C6H5Cl.value:
            return "DimerZOrbitalordnung-C6H5Cl-C2v-gesamt-MO-beiWW.pdf"
        if self.value == Molecule.C6H5Cl_rotated.value:
            return "DimerZOrbitalordnung-C6H5Cl-C2h-gesamt-MO-beiWW.pdf"
        return ""

    def get_ci_vectors_triplets(self):
        if self.value == Molecule.C6H6.value:
            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b1u": 1, "b2g": 2, "b3g": 1, "au": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b1u": 0, "b2g": 1, "b3g": 2, "au": 1})

            triplet_1 = MonomerState(label="i^3 b_{2u}", symmetry_index=3, point_group=self.get_point_group())
            triplet_1.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                      additive_monomer_occupation=additive_m,
                                      combination=SIGN.MINUS)
            triplet_2 = MonomerState(label="e^3 b_{2u}", symmetry_index=3, point_group=self.get_point_group())
            triplet_2.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                      additive_monomer_occupation=additive_m,
                                      combination=SIGN.PLUS)
            #

            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b1u": 1, "b2g": 1, "b3g": 2, "au": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b1u": 0, "b2g": 2, "b3g": 1, "au": 1})

            triplet_3 = MonomerState(label="e^3 b_{3u}", symmetry_index=2, point_group=self.get_point_group())
            triplet_3.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.MINUS)
            triplet_4 = MonomerState(label="i^3 b_{3u}", symmetry_index=2, point_group=self.get_point_group())
            triplet_4.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.PLUS)
        # elif self.value == Molecule.C6H5Cl.value or self.value == Molecule.C6H5Cl_rotated.value:
        #     # <- same triplet calculation since these are monomer properties
        #     first_sym = 1
        #     always_positive_ci_part_1stsym = {"b2": 1, "b2*": 1, "a2": 2, "a2*": 0}
        #     sign_changing_ci_part_1stsym = {"b2": 2, "b2*": 0, "a2": 1, "a2*": 1}
        #     name_1, initial_combination_1 = "$i^3 a_1$", "-"  # state 1 in sym 1
        #     name_2, initial_combination_2 = "$e^3 a_1$", "+" # state 2 in sym 1
        #
        #     second_sym = 2
        #     always_positive_ci_part_2ndsym = {"b2": 2, "b2*": 1, "a2": 1, "a2*": 0}
        #     sign_changing_ci_part_2ndsym = {"b2": 1, "b2*": 0, "a2": 2, "a2*": 1}
        #     name_3, initial_combination_3 = "$e^3 b_{1}$", "+" # state 1 in sym 2
        #     name_4, initial_combination_4 = "$i^3 b_{1}$", "-" # state 2 in sym 2
        else:
            raise Exception("to be defined: triplet ci vectors")

        # # combine information:
        # sym_1 = {
        #     "sym": first_sym,
        #     "occupied_mos": self.get_occupied_mos_for_both_ci_parts(
        #         always_positive_ci_part=always_positive_ci_part_1stsym,
        #         sign_changing_ci_part=sign_changing_ci_part_1stsym),
        #     "included states": [(name_1, initial_combination_1),
        #                         (name_2, initial_combination_2)]
        # }
        # sym_2 = {
        #     "sym": second_sym,
        #     "occupied_mos": self.get_occupied_mos_for_both_ci_parts(
        #         always_positive_ci_part=always_positive_ci_part_2ndsym,
        #         sign_changing_ci_part=sign_changing_ci_part_2ndsym),
        #     "included states": [(name_3, initial_combination_3),
        #                         (name_4, initial_combination_4)]
        # }
        return [triplet_1, triplet_2, triplet_3, triplet_4]

from enum import Enum

from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.building_blocks.MonomerState import MonomerState
from src.mathematics_and_combinations.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class Molecule(Enum):
    C6H6 = "Benzene"
    C6H5Cl = "Chlorobenzene"
    C6H5Cl_rotated = "Chlorobenzene(rotated)"

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
        s = MonomerOccupation(point_group=self.get_point_group())
        s.set_occupation({"left_bottom": 2, "right_bottom": 2, "left_top": 0, "right_top": 0})
        singlet = MonomerState(label="S", molpro_symmetry_number=1, point_group=self.get_point_group())
        singlet.set_monomer_occupations(always_positive_monomer_occupation=s,
                                      additive_monomer_occupation=None, combination=SIGN.PLUS)

        q = MonomerOccupation(point_group=self.get_point_group())
        q.set_occupation({"left_bottom": 1, "right_bottom": 1, "left_top": 1, "right_top": 1})
        quintet = MonomerState(label="Q", molpro_symmetry_number=1, point_group=self.get_point_group())
        quintet.set_monomer_occupations(always_positive_monomer_occupation=q,
                                        additive_monomer_occupation=None, combination=SIGN.PLUS)


        if self.value == Molecule.C6H6.value:
            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b1u": 1, "b2g": 2, "b3g": 1, "au": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b1u": 0, "b2g": 1, "b3g": 2, "au": 1})

            triplet_1 = MonomerState(label="i^3 b_{2u}", molpro_symmetry_number=3, point_group=self.get_point_group())
            triplet_1.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                      additive_monomer_occupation=additive_m,
                                      combination=SIGN.MINUS)
            triplet_2 = MonomerState(label="e^3 b_{2u}", molpro_symmetry_number=3, point_group=self.get_point_group())
            triplet_2.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                      additive_monomer_occupation=additive_m,
                                      combination=SIGN.PLUS)

            #

            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b1u": 1, "b2g": 1, "b3g": 2, "au": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b1u": 0, "b2g": 2, "b3g": 1, "au": 1})

            triplet_3 = MonomerState(label="e^3 b_{3u}", molpro_symmetry_number=2, point_group=self.get_point_group())
            triplet_3.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.MINUS)
            triplet_4 = MonomerState(label="i^3 b_{3u}", molpro_symmetry_number=2, point_group=self.get_point_group())
            triplet_4.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.PLUS)
        elif self.value == Molecule.C6H5Cl.value or self.value == Molecule.C6H5Cl_rotated.value:
            # <- same triplet calculation since these are monomer properties

            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b2": 1, "b2*": 1, "a2": 2, "a2*": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b2": 2, "b2*": 0, "a2": 1, "a2*": 1})

            triplet_1 = MonomerState(label="i^3 a_1", molpro_symmetry_number=1, point_group=self.get_point_group())
            triplet_1.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.MINUS)
            triplet_2 = MonomerState(label="e^3 a_1", molpro_symmetry_number=1, point_group=self.get_point_group())
            triplet_2.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.PLUS)

            #

            always_positive_m = MonomerOccupation(point_group=self.get_point_group())
            always_positive_m.set_occupation({"b2": 2, "b2*": 1, "a2": 1, "a2*": 0})
            additive_m = MonomerOccupation(point_group=self.get_point_group())
            additive_m.set_occupation({"b2": 1, "b2*": 0, "a2": 2, "a2*": 1})

            triplet_3 = MonomerState(label="i^3 b_{1}", molpro_symmetry_number=2, point_group=self.get_point_group())
            triplet_3.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.MINUS)
            triplet_4 = MonomerState(label="e^3 b_{1}", molpro_symmetry_number=2, point_group=self.get_point_group())
            triplet_4.set_monomer_occupations(always_positive_monomer_occupation=always_positive_m,
                                              additive_monomer_occupation=additive_m,
                                              combination=SIGN.PLUS)
        else:
            raise Exception("to be defined: triplet ci vectors")

        return [singlet, quintet, triplet_1, triplet_2, triplet_3, triplet_4]

from enum import Enum

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

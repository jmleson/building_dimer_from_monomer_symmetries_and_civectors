from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP
from src.symmetries.ordering_orbitals_by_symmetry_order import ordering_orbitals_by_symmetry_order


class DimerDeterminant(object):

    def __init__(self, orbital_symmetry_labels:list[str], sign:SIGN, point_group:POINTGROUP, ordering:CI_ORDERING):
        self.point_group = point_group
        # sort first:
        orbitals = [Orbital(sym_label=i.replace("-","").replace("+",""), occupation=1, point_group=point_group)
                         for i in orbital_symmetry_labels]
        self.orbitals = ordering_orbitals_by_symmetry_order(orbitals=orbitals, ordering=ordering, point_group=self.point_group)

        self.sign = sign
        self.prefactor = 1

    def get_factor(self):
        if self.sign == SIGN.PLUS:
            return abs(self.prefactor)
        return - abs(self.prefactor)

    def set_factor(self, factor):
        if factor < 0:
            self.sign = SIGN.MINUS
        else:
            self.sign = SIGN.PLUS
        self.prefactor = abs(factor)

    def determine_symmetry(self):
        sym = self.point_group.total_symmetric
        for i in self.orbitals:
            sym = self.point_group.product(sym, i.sym_label)
        return sym

    def determinants_string(self):
        eq = self.sign.value
        if self.prefactor != 1:
            eq += str(abs(self.prefactor)) + r" \cdot{} "
        eq += r" \left| "
        eq += r"\underbrace{ "
        inbetween = "".join(
            [format_irred_representations(i.sym_label) for i in self.orbitals ]
        )
        eq += inbetween + " }_{" + format_irred_representations(self.determine_symmetry())  + r"}"
        return eq + r"\right|"


    def addable(self, other):
        if not isinstance(other, DimerDeterminant):
            return False
        if self.point_group.value != other.point_group.value:
            return False
        if len(self.orbitals) != len(other.orbitals):
            return False
        for i in range(len(self.orbitals)):
            if self.orbitals[i] != other.orbitals[i]:
                return False
        return True

    def __eq__(self, other):
        if not self.addable(other):
            return False
        if self.prefactor != other.prefactor:
            return False
        return True



from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP
from src.symmetries.ordering_orbitals_by_symmetry_order import ordering_orbitals_by_symmetry_order


class DimerDeterminant(object):

    def __init__(self, orbital_symmetry_labels:list[str], sign:SIGN, point_group:POINTGROUP, ordering:CI_ORDERING):
        self.point_group = point_group
        self.ordering = ordering

        self.single_occupied_orbitals = self.format_orbitals_with_occupation_x(orbital_symmetry_labels=orbital_symmetry_labels, occupation=1)

        self.orbitals_of_even_electron_number = []

        self.sign = sign
        self.prefactor = 1


    def format_orbitals_with_occupation_x(self, orbital_symmetry_labels, occupation:int):
        orbitals = [Orbital(sym_label=i.replace("-", "").replace("+", ""), occupation=occupation, point_group=self.point_group)
                    for i in orbital_symmetry_labels]
        return ordering_orbitals_by_symmetry_order(orbitals=orbitals, ordering=self.ordering,
                                                                            point_group=self.point_group)


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
        for i in self.single_occupied_orbitals:
            sym = self.point_group.product(sym, i.sym_label)
        return sym

    def determinants_string(self):
        eq = self.sign.value
        if self.prefactor != 1:
            eq += str(abs(self.prefactor)) + r" \cdot{} "
        eq += r" \left| "
        eq += r"\underbrace{ "
        inbetween = "".join(
            [format_irred_representations(i.sym_label) for i in self.single_occupied_orbitals]
        )
        eq += inbetween + " }_{" + format_irred_representations(self.determine_symmetry())  + r"}"
        return eq + r"\right|"


    def addable(self, other):
        if not isinstance(other, DimerDeterminant):
            return False
        if self.point_group.value != other.point_group.value:
            return False
        if len(self.single_occupied_orbitals) != len(other.single_occupied_orbitals):
            return False
        for i in range(len(self.single_occupied_orbitals)):
            if self.single_occupied_orbitals[i] != other.single_occupied_orbitals[i]:
                return False
        return True

    def latex_ci_equation(self, ordering: CI_ORDERING):
        if len(self.orbitals_of_even_electron_number) == 0:
            raise Exception("orbital of occupation != 1 have to be set for this")

        # determine which orbitals have a known occupation which not:
        definite_orbitals = {}
        ambiguous_orbitals = []
        from collections import Counter
        count = Counter(self.orbitals_of_even_electron_number+self.single_occupied_orbitals)
        for orbital, n in count.items():
            if n == 2:
                if orbital.sym_label in definite_orbitals.keys():
                    raise Exception("?")
                definite_orbitals[orbital.sym_label] = orbital.occupation
            else:
                ambiguous_orbitals.append(orbital)

        # find out choices for orbitals without known occupation:
        ambiguous_orbitals = sorted(ambiguous_orbitals, key=lambda o: o.sym_label)
        ambiguous_orbitals_dict = {}
        for o in ambiguous_orbitals:
            if o.sym_label not in ambiguous_orbitals_dict:
                ambiguous_orbitals_dict[o.sym_label] = []
            ambiguous_orbitals_dict[o.sym_label].append(o.occupation)

        # for i in self.point_group.choices_irreduzible_representations_molpro_ordered:
        #     if i in


        return "tbi"

    def __eq__(self, other):
        if not self.addable(other):
            return False
        if self.prefactor != other.prefactor:
            return False
        return True



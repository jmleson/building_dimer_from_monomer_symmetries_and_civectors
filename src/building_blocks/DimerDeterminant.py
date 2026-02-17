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
        if self.get_factor() != 1 and self.get_factor() != -1:
            eq += str(abs(self.prefactor)) + r" \cdot{} "
        eq += r" \left| "
        eq += r"\underbrace{ "
        inbetween = "".join(
            [format_irred_representations(i.sym_label) for i in self.single_occupied_orbitals]
        )
        eq += inbetween + " }_{" + format_irred_representations(self.determine_symmetry())  + r"}"
        return eq + r"\right|"


    def addable(self, other, regarding:str):
        if regarding not in ["symmetry", "ci vector"]:
            raise Exception("parameter 'regarding' has to choose symmetry / ci vector notation")
        if not isinstance(other, DimerDeterminant):
            return False
        if self.point_group.value != other.point_group.value:
            return False
        if len(self.single_occupied_orbitals) != len(other.single_occupied_orbitals):
            return False
        for i in range(len(self.single_occupied_orbitals)):
            if self.single_occupied_orbitals[i] != other.single_occupied_orbitals[i]:
                return False
        if regarding == "ci vector":
            if len(self.orbitals_of_even_electron_number) != len(other.orbitals_of_even_electron_number):
                return False
            for i in range(len(self.orbitals_of_even_electron_number)):
                if self.orbitals_of_even_electron_number[i] != other.orbitals_of_even_electron_number[i]:
                    return False
        return True

    def find_orbital(self, sym_label:str):
        orbitals = self.single_occupied_orbitals + self.orbitals_of_even_electron_number
        for o in orbitals:
            if o.sym_label == sym_label:
                return o
        return None

    def latex_ci_equation(self, ordering: CI_ORDERING):
        if len(self.orbitals_of_even_electron_number) == 0:
            raise Exception("orbital of occupation != 1 have to be set for this")
        if len(self.single_occupied_orbitals + self.orbitals_of_even_electron_number) > 8:
            raise Exception("more than 8 orbitals impossible ")

        if ordering == CI_ORDERING.molpro:
            order = self.point_group.choices_irreduzible_representations_molpro_ordered
        else:
            raise Exception("nyi")


        s = ""
        for orbital_sym in order:
            orbital = self.find_orbital(sym_label=orbital_sym)
            if orbital is None:
                orbital = Orbital(sym_label=orbital_sym, occupation=2, point_group=self.point_group)
            s+= orbital.get_occupation_string()

        if self.get_factor() != 1 and self.get_factor() != -1:
            return self.sign.value + str(abs(self.prefactor)) + r" \cdot \left|" + s + r"\right|"
        return self.sign.value + r"\left|" + s + r"\right|"

    def __eq__(self, other):
        if not self.addable(other, regarding="ci vector"):
            return False
        if self.prefactor != other.prefactor:
            return False
        if self.sign != other.sign:
            return False
        return True



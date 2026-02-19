from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.Orbital import Orbital
from src.latex.format_irred_representations import format_irred_representations
from src.latex.underbrace import underbrace
from src.mathematics_and_combinations.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP
from src.symmetries.ordering_orbitals_by_symmetry_order import ordering_orbitals_by_symmetry_order


class DimerDeterminant(object):

    def __init__(self, orbital_symmetry_labels_occ1:list[str], orbital_symmetry_labels_occ0:list[str],
                 sign:SIGN, point_group:POINTGROUP, ordering:CI_ORDERING):
        self.point_group = point_group
        self.ordering = ordering

        self.single_occupied_orbitals = self._format_orbitals_with_occupation_x(orbital_symmetry_labels=orbital_symmetry_labels_occ1, occupation=1)
        self.unoccupied_orbitals = self._format_orbitals_with_occupation_x(orbital_symmetry_labels=orbital_symmetry_labels_occ0, occupation=0)

        self.sign = sign
        self.prefactor = 1

        self._check_number_of_electrons()


    def _format_orbitals_with_occupation_x(self, orbital_symmetry_labels, occupation:int):
        orbitals = [Orbital(sym_label=i.replace("-", "").replace("+", ""), occupation=occupation, point_group=self.point_group)
                    for i in orbital_symmetry_labels]
        return ordering_orbitals_by_symmetry_order(orbitals=orbitals, ordering=self.ordering, point_group=self.point_group)

    def _check_number_of_electrons(self):
        number_of_electrons = 0
        for orbital_sym in self.point_group.irreduzible_representations_molpro_ordered:# order does not matter
            orbital = self.find_orbital(sym_label=orbital_sym)
            if orbital is None:
                number_of_electrons += 2
            else:
                number_of_electrons += orbital.occupation
        if number_of_electrons != 8:
            print(self.latex_ci_equation(),"\t"," electrons =", number_of_electrons, flush=True)
            # print("!!! number_of_electrons should be 8")
            raise Exception("number_of_electrons should be 8")

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
            sym = self.point_group.product(sym, i.sym_label.replace("*",""))
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
            if len(self.unoccupied_orbitals) != len(other.unoccupied_orbitals):
                return False
            for i in range(len(self.unoccupied_orbitals)):
                if self.unoccupied_orbitals[i] != other.unoccupied_orbitals[i]:
                    return False
        return True

    def find_orbital(self, sym_label:str):
        orbitals = self.single_occupied_orbitals + self.unoccupied_orbitals
        for o in orbitals:
            if o.sym_label == sym_label:
                return o
        return None

    def latex_ci_equation(self, short_version:bool=False):
        if len(self.single_occupied_orbitals + self.unoccupied_orbitals) > 8:
            raise Exception("more than 8 orbitals are impossible")

        if self.ordering == CI_ORDERING.molpro:
            order = self.point_group.irreduzible_representations_molpro_ordered
        else:
            order = self.point_group.irreduzible_representations_orbital_ordered

        s = ""
        for orbital_sym in order:
            orbital = self.find_orbital(sym_label=orbital_sym)
            if orbital is None:
                orbital = Orbital(sym_label=orbital_sym, occupation=2, point_group=self.point_group)
            s += orbital.get_occupation_string(multiplied_out=False, molpro_notation=short_version)

        if not short_version:
            main = underbrace(s, info=self.determine_symmetry())
            main = format_irred_representations(main)
        else:
            main = s
        if self.get_factor() != 1 and self.get_factor() != -1:
            return self.sign.value + str(abs(self.prefactor)) + r" \cdot \left|" + main + r"\right|"
        return self.sign.value + r"\left|" + main + r"\right|"

    def __eq__(self, other):
        if not self.addable(other, regarding="ci vector"):
            return False
        if self.prefactor != other.prefactor:
            return False
        if self.sign != other.sign:
            return False
        return True



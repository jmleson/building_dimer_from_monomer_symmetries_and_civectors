import copy

from src.CI_ORDERING import CI_ORDERING
from src.DimerOccupation import DimerOccupation
from src.building_blocks.MonomerState import MonomerState
from src.latex.bold import bold
from src.mathematics.Sign import SIGN
from src.latex.get_array_environment import get_array_environment
from src.latex.latex_equation_types import latex_equation_types, get_expression_as_latex_formula
from src.symmetries.POINTGROUP import POINTGROUP


class DimerState:

    def __init__(self, monomer_state_1: MonomerState, monomer_state_2: MonomerState, combination:SIGN, point_group:POINTGROUP, ordering:CI_ORDERING):
        self.monomer_state_1 = monomer_state_1
        self.monomer_state_2 = monomer_state_2
        self.combination = combination

        self.point_group = point_group
        self.ordering = ordering

        self.dimer_occupations = []

        self.full_list_of_determinants = []
        self.summed_up_list_of_determinants_sym = []
        self.summed_up_list_of_determinants_ci = []

        self.symmetry = "unknown"


    def get_label(self):
        if self.monomer_state_1 == self.monomer_state_2:
            label = f"{self.monomer_state_1.label} * {self.monomer_state_2.label}"
        else:
            label = f"{self.monomer_state_1.label} * {self.monomer_state_2.label} {self.combination.value} {self.monomer_state_2.label} * {self.monomer_state_1.label}"
        return label


    def get_product_terms(self):
        # first combination:
        for sign_i, i in [(SIGN.PLUS, self.monomer_state_1.always_positive_monomer_occupation),
                   (self.monomer_state_1.combination, self.monomer_state_1.additive_monomer_occupation)]:
            for sign_j, j in [(SIGN.PLUS, self.monomer_state_2.always_positive_monomer_occupation),
                  (self.monomer_state_2.combination, self.monomer_state_2.additive_monomer_occupation)]:
                if i is not None and j is not None:
                    sign = SIGN.PLUS if sign_i == sign_j else SIGN.MINUS
                    d = DimerOccupation(i, j, sign=sign, point_group=self.point_group)
                    self.dimer_occupations.append(d)
                    if self.monomer_state_1 != self.monomer_state_2:
                        sign = SIGN.PLUS if sign == self.combination else SIGN.MINUS
                        d = DimerOccupation(j, i, sign=sign, point_group=self.point_group)
                        self.dimer_occupations.append(d)
                # else: S-Q case
                #     print(self.monomer_state_1.get_multiplicity(), self.monomer_state_2.get_multiplicity(), flush=True)


    def to_latex(self, detailed:bool=False):
        eq = get_expression_as_latex_formula(self.get_label() , latex_equation_types.BASIC) + "\n"
        eq += get_expression_as_latex_formula(self.latex_picture(draw_label=False), latex_equation_types.BASIC) + "\n"

        if not detailed:# otherwise the printing function do this automatically
            self.get_determinants()
            self.sum_up_determinants()

        eq += "\n" + bold("written in CI vectors:") + "\n\n"
        if detailed:
            eq += "monomer ci vectors:\n"
            eq += self.written_in_monomer_ci_vectors()
            eq += "substitution by dimer:\n"
            eq += self.written_in_dimer_ci_vectors(summed_up=False)
            eq += "summed up:\n"
        eq += self.written_in_dimer_ci_vectors(summed_up=True)

        eq += "\n" + bold("or, expressed in terms of symmetry:") + "\n\n"
        if detailed:
            eq += "monomer determinants:\n"
            eq += self.monomer_determinants(multiplied_out=False)
            eq += "substitution by dimer:\n"
            eq += self.monomer_determinants(multiplied_out=True)
            eq += "multiplied out:\n"
            eq += self.get_multiplied_out_determinants(summed_up=False)
            eq += "summed up:\n"

        eq += self.get_multiplied_out_determinants(summed_up=True)

        return eq + "\n" + r"\vspace{0.5cm}" + "\n"


    def get_determinants(self):
        full_list_of_determinants = []
        for i in self.dimer_occupations:
            i.multiply_out(ordering=self.ordering)
            full_list_of_determinants.extend(i.determinants)
        self.full_list_of_determinants = full_list_of_determinants

    def sum_up_regarding(self, regarding:str):
        list_of_determinants = []
        used_indices = []
        for i in range(len(self.full_list_of_determinants)):
            factor = self.full_list_of_determinants[i].get_factor()
            if i in used_indices:
                continue
            for j in range(i + 1, len(self.full_list_of_determinants)):
                if self.full_list_of_determinants[i].addable(self.full_list_of_determinants[j], regarding=regarding):
                    used_indices.append(j)
                    factor += self.full_list_of_determinants[j].get_factor()
            if factor != 0:
                copied_det = copy.deepcopy(self.full_list_of_determinants[i])
                copied_det.set_factor(factor)
                list_of_determinants.append(copied_det)
            used_indices.append(i)
        return list_of_determinants

    def sum_up_determinants(self):
        self.summed_up_list_of_determinants_sym = self.sum_up_regarding(regarding="symmetry")
        self.summed_up_list_of_determinants_ci = self.sum_up_regarding(regarding="ci vector")

        sym = set([det.determine_symmetry() for det in self.summed_up_list_of_determinants_sym])
        if len(sym) == 1:
            self.symmetry = list(sym)[0]
        elif len(sym) == 0:
            self.symmetry = self.point_group.total_symmetric
        else:
            raise Exception(f"no symmetry found: more than one symmetry remaining {sym}")
        return



    def get_multiplied_out_determinants(self, summed_up:bool = False):#
        if not summed_up:
            self.get_determinants()
            list_of_determinants = self.full_list_of_determinants
        else:
            self.sum_up_determinants()
            list_of_determinants = self.summed_up_list_of_determinants_sym

        full_list_of_determinants = [det.determinants_string() for det in list_of_determinants]
        eq = get_array_environment(full_list_of_determinants, breaking_after=6)
        return get_expression_as_latex_formula(eq, latex_equation_types.MULTLINE)+"\n"



    def written_in_dimer_ci_vectors(self, summed_up:bool=False) -> str:
        if not summed_up:
            self.get_determinants()
            list_of_determinants = self.full_list_of_determinants
        else:
            self.sum_up_determinants()
            list_of_determinants = self.summed_up_list_of_determinants_ci

        full_list_of_determinants = [det.latex_ci_equation(ordering=self.ordering) for det in list_of_determinants]
        eq = get_array_environment(full_list_of_determinants, breaking_after=6)
        return get_expression_as_latex_formula(eq, latex_equation_types.MULTLINE)+"\n"

    def written_in_monomer_ci_vectors(self) -> str:
        eq = get_array_environment([d.written_in_monomer_ci_vectors(ordering=self.ordering) for d in self.dimer_occupations],
                                   breaking_after=4)
        return get_expression_as_latex_formula(eq, latex_equation_types.DISPLAYED)

    def monomer_determinants(self, multiplied_out:bool):
        eq = get_array_environment([i.monomer_determinants(multiplied_out=multiplied_out) for i in self.dimer_occupations],
                                   breaking_after=4 if not multiplied_out else 2)
        return get_expression_as_latex_formula(eq, latex_equation_types.MULTLINE)


    def latex_picture(self,draw_label:bool=False):
        eq = get_array_environment([i.latex_picture(draw_label=draw_label) for i in self.dimer_occupations])
        return eq


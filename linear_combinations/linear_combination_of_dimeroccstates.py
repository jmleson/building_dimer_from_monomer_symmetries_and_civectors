from typing import List

from symmetrie_und_orbitale.PointGroups import POINTGROUP
from symmetrie_und_orbitale.term_step import term_step
from symmetrie_und_orbitale.dimer_occ_state import dimer_occ_state
from symmetrie_und_orbitale.format_irred_representations import format_irred_representations
from symmetrie_und_orbitale.latex_equation_types import latex_equation_types, get_expression_as_latex_formula
from symmetrie_und_orbitale.signed_number_to_latex_number import signed_number_to_latex_number
from symmetrie_und_orbitale.switch_monomers import switch_monomers



class linear_combination_of_dimeroccstates:

    def __init__(self, dimeroccstates:List[dimer_occ_state]):
        self.dimer_occ_states = dimeroccstates
        self.name = ""

    def add(self, other):
        for d in other.dimer_occ_states:
            self.dimer_occ_states.append(d)
    def change_sign(self):
        for d in range(len(self.dimer_occ_states)):
            self.dimer_occ_states[d].sign_and_factor = -self.dimer_occ_states[d].sign_and_factor
            self.dimer_occ_states[d].set_up()

    def change_combination(self):
        """ ehemals über self.state (positive Kombi, wenn True; negative, wenn False) geregelt """
        if len(self.dimer_occ_states) != 2:
            raise Exception("not yet implemented; unsure what to do with this")
        self.dimer_occ_states[-1].sign_and_factor = -self.dimer_occ_states[-1].sign_and_factor
        self.dimer_occ_states[-1].set_up()

    def draw(self) -> str:
        equation= " "
        if len(self.dimer_occ_states) > 4:
            equation += r"\begin{array}{c}"
        for i in range(len(self.dimer_occ_states)):
            state = self.dimer_occ_states[i]
            equation += signed_number_to_latex_number(state.sign_and_factor)
            equation += r"\left(\text{"+state.get_total_mo_schemata(as_raw_ticzpicture=True)+r"}\right)"
            if (i+1) % 4 == 0:# nach Index 4, 8, ...
                equation += r"\\\\"
        if len(self.dimer_occ_states) > 4:
            equation += r"\end{array}"
        return get_expression_as_latex_formula(equation, latex_equation_types.BASIC)

    def check_valitity(self):
        if len(self.dimer_occ_states) <= 1:
            return False
        if (len(self.dimer_occ_states) == 2 and
                self.dimer_occ_states[0].occupied_mos == self.dimer_occ_states[1].occupied_mos  # links & rechts gl. Zustand
                and self.dimer_occ_states[0].sign_and_factor != self.dimer_occ_states[1].sign_and_factor):
            return False
        return True

    def build_linear_kombination(self, detailed:bool=False):
        if not self.check_valitity():
            return
        parts= []
        for i in self.dimer_occ_states:
            for j in i.get_parts():
                parts.append(j)

        # print("after sign switch:\n\t", parts,"\n")
        result = self.dimer_occ_states[0].resolve_duplicates(parts)
        if detailed:
            equation = r"="
            equation_determinants = "\n"+r"\begin{array}{l}"+"\n"
            for i in range(len(self.dimer_occ_states)):
                part = self.dimer_occ_states[i]
                equation += signed_number_to_latex_number(part.sign_and_factor) + r"\left("+ part.initial_equation["sorted_formatted"] + r"\right)"

                equation_determinants += signed_number_to_latex_number(part.sign_and_factor) + r"\left( \begin{array}{c} " + "\n"
                equation_determinants += part.latex_equation[term_step.EVALUATED.value].replace("=","") + "\n"
                equation_determinants += r"\end{array}" + r"\right)" + r"\\" + "\n"

            equation_determinants += r"\end{array}"+"\n"
            equation_determinants = get_expression_as_latex_formula(format_irred_representations(equation_determinants), latex_equation_types.DISPLAYED)
            formatted_equation = get_expression_as_latex_formula(format_irred_representations(equation), latex_equation_types.MULTLINE)
        combined, lines, latex_equation = self.dimer_occ_states[0].get_equational_form(result,detailed=True)
        result = get_expression_as_latex_formula(format_irred_representations(latex_equation), latex_equation_types.MULTLINE)
        if len(result) == 0:
            result = r"$=0 \quad\Rightarrow a_g $"
        if detailed:
            if len(self.dimer_occ_states) <= 2:
                return formatted_equation+"\n"+result + "\n"+ r"\\\\"+"\n\n"
            return equation_determinants+"\n"+result + "\n"+ r"\\\\"+"\n\n"
        return result + r"\\\\"+"\n\n"

    def get_info_about_involved_monomer_symmetries(self):
        all_symmetries = []
        for i in self.dimer_occ_states:
            all_symmetries += i.monomer_symmetries
        all_symmetries = list(set(all_symmetries))# remove duplicates
        for i in range(len(all_symmetries)):
            all_symmetries[i] = format_irred_representations(all_symmetries[i])
        return f"enthaltene Monomer-Symmetrien = ${','.join(all_symmetries)}$"



if __name__ == "__main__":
    occupied_mos = {
        "b1u": {"left": 0, "right": 0},
        "au": {"left": 1, "right": 1},
        "b2g": {"left": 1, "right": 2},
        "b3g": {"left": 2, "right": 1},
    }
    d1 = dimer_occ_state(occupied_mos=occupied_mos, point_group=POINTGROUP.D2h)
    d2 = dimer_occ_state(switch_monomers(occupied_mos),-1)

    l = linear_combination_of_dimeroccstates([d1,d2])
    l.draw()
    l.build_linear_kombination(True)
    print(l.draw())
    print(l.build_linear_kombination())

    # l.state = False
    # l.draw()
    # l.build_linear_kombination()
    # print(l.draw())
    # print(l.build_linear_kombination())
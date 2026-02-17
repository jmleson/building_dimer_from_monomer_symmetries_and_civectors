import copy
from typing import Dict, List

from src.latex.latex_equation_types import get_expression_as_latex_formula, latex_equation_types
from src_alongLaTex.symmetries.group_theory.PointGroups import POINTGROUP
from src_alongLaTex.symmetries.basisclass_handeling_mos import handeling_mos
from src_alongLaTex.symmetries.general_functionalities.monomer_positions import MonomerPositions
from src_alongLaTex.symmetries.mathematics.term_step import term_step
from src_alongLaTex.latex.format_irred_representations import format_irred_representations
from src_alongLaTex.get_mo_schema import get_total_mo_schemata
from src_alongLaTex.symmetries.group_theory.get_total_symmety_from_list_of_irred import get_total_symmety_from_list_of_irred
from src_alongLaTex.latex.signed_number_to_latex_number import signed_number_to_latex_number
from src_alongLaTex.symmetries.mathematics.split_expression_into_sums import split_expression_into_sums, split_sum_into_parts
from src_alongLaTex.symmetries.mathematics.switch_monomers import switch_monomers


class dimer_occ_state(handeling_mos):
    """
    state of two monomer orbital configuration = unit / set of single_occupied_orbitals
    """

    def __init__(self, point_group: POINTGROUP, occupied_mos:Dict, sign_and_factor:int=+1) -> None:
        """

        :param occupied_mos: dictionary carrying the occupation numbers of the monomers
        :param sign_and_factor:
        """
        super().__init__(point_group)
        self.sign_and_factor = sign_and_factor
        self.occupied_mos = occupied_mos
        self.set_up()


    def set_up(self) -> None:
        """
        calculation the basic equations describing this dimer state
        used to initialze or reset a dimer_occ_state object
        :return:
        """
        self.initial_equation = {"plain": "", "formatted": "", "sorted": "", "sorted_formatted": ""}
        self.dimermo_equation = {"plain": "",#<- abstammend von "sorted" vom Monomer, aber noch nicht neu sortiert
                               "formatted": ""}
        self.split_factors = None # aufgeteilte Produktterme TODO
        self.monomer_symmetries = []

        self.set_initial_equations()
        self.set_equation_as_dimer_orbitals()
        self.latex_equation = {}
        self.ausklammern_latex_equation_of_orbital_symmetry(term_step.COMBINED)
        self.ausklammern_latex_equation_of_orbital_symmetry(term_step.SORTED)
        self.ausklammern_latex_equation_of_orbital_symmetry(term_step.EVALUATED)


    def get_total_mo_schemata(self,as_raw_ticzpicture:bool=False) -> str:
        """
        getting a latex formatted drawing of the single_occupied_orbitals and their occupations
        :param as_raw_ticzpicture: when False, mo schema is added with prefactor and parentheses
        :return: mo diagramm (tikz)
        """
        if as_raw_ticzpicture:
            return get_total_mo_schemata(self.point_group, self.occupied_mos)
        sign = signed_number_to_latex_number(self.sign_and_factor)
        eq = sign + r"\left(" + get_total_mo_schemata(self.point_group, self.occupied_mos) + r"\right)"
        return get_expression_as_latex_formula(eq, latex_equation_types.BASIC)


    def set_initial_equations(self) -> None:
        """
        calculate the equation that is at the start of the calculation = single occupied single_occupied_orbitals that are relevant for the determinant
        :return: (initial_equation is set up)
        """
        left = []
        right = []
        left_sym = []
        right_sym = []
        for i in self.occupied_mos.items():
            key, value = i[0], i[1]
            if value[MonomerPositions.left] == 1:
                left.append("(" + key + "^{l})")
                left_sym.append(key)
            if value[MonomerPositions.right] == 1:
                right.append("(" + key + "^{r})")
                right_sym.append(key)
        # Symmetrie der Monomere berechnen:
        total = left + right
        left_sym = get_total_symmety_from_list_of_irred(left_sym,self.point_group)
        right_sym = get_total_symmety_from_list_of_irred(right_sym,self.point_group)
        self.add_monomer_sym(left_sym)
        self.add_monomer_sym(right_sym)
        # sort:
        choices = []
        for i in self.point_group.choices_irreduzible_representations_molpro_ordered_monomer:
            choices.append("(" + i + "^{l})")
            choices.append("(" + i + "^{r})")
        sorted_combination = sorted(total, key=lambda x: choices.index(x))

        # Ausgabe formatieren:
        self.initial_equation["plain"] = " ".join(left) + " " + " ".join(right)
        self.initial_equation["sorted"] = " ".join(sorted_combination)
        self.initial_equation["sorted_formatted"] = r" \cdot ".join(sorted_combination)
        left_part = r"\cdot ".join(left)
        left_part = r"\underbrace{" + left_part + r"}_{\text{l: }" + left_sym + r"}"
        right_part = r"\cdot ".join(right)
        right_part = r"\underbrace{" + right_part + r"}_{\text{r: }" + right_sym + r"}"
        if len(left) > 0 and len(right) > 0:
            self.initial_equation["formatted"] = left_part + r"\cdot " + right_part
        elif len(left) > 0:
            self.initial_equation["formatted"] = left_part
        elif len(right) > 0:
            self.initial_equation["formatted"] = right_part
        else:
            raise Exception("should not be able to happen")
        self.initial_equation["sorted_formatted"] = r"\left|" + self.initial_equation["sorted_formatted"] + r"\right|"
        return


    def combine_terms(self) -> None:
        """
        calculate the summands that arise from the initial equation of single occupied dimer single_occupied_orbitals
        :return: (dimermo_equation is set up)
        """
        combined_terms, sorted_terms, combined_sorted_evaluated = super().combine_terms(split_factors=self.split_factors)
        self.dimermo_equation["combined_all"] = [{**d, "amount": d["amount"] * self.sign_and_factor} for d in combined_terms]
        self.dimermo_equation["sorted_all"] = [{**d, "amount": d["amount"] * self.sign_and_factor} for d in sorted_terms]
        self.dimermo_equation["combined_sorted_evaluated"] = [{**d, "amount": d["amount"] * self.sign_and_factor} for d in combined_sorted_evaluated]


    def get_parts(self) -> List[Dict]:
        """
        get list of included determinant terms (amount, factors, forbidden)
        :return:
        """
        parts = []
        for j in self.dimermo_equation["combined_sorted_evaluated"]:
            new = copy.deepcopy(j)
            if not new["forbidden"]:
                parts.append(new)
        return parts # TODO Funktion auch in dieser Klasse nutzen (s. Vorzeichen!)


    def set_equation_as_dimer_orbitals(self) -> None:
        r"""
        convert equation of monomer-single_occupied_orbitals into corresponding dimer orbital combination:
        replaces e.g. a_u^{r} by something like b2u-b2g
        :return:
            dimermo_equation.formatted enthält \cdot zwischen Termen, formatted hat Determinantenstriche
            plain = reine Multiplikationsterme (in Klammern) -> für weitere Berechnungen nötig
        """
        dimer_equation_formatted = self.initial_equation["sorted_formatted"]
        self.dimermo_productterm = self.initial_equation["sorted"]
        for replacement in self.point_group.mo_pairs.items():
            dimer_equation_formatted = dimer_equation_formatted.replace(replacement[0], replacement[1])
            self.dimermo_productterm = self.dimermo_productterm.replace(replacement[0], replacement[1])
        self.dimermo_equation["formatted"] = dimer_equation_formatted
        self.split_factors = split_sum_into_parts(split_expression_into_sums(self.dimermo_productterm))


    def ausklammern_latex_equation_of_orbital_symmetry(self, evaluated: term_step = term_step.COMBINED) -> None:
        """
        combine the determinants if possible and set the result as a latex_equation item
        :param evaluated: which evaluation step is needed
        :return:
        """
        self.combine_terms()
        if evaluated == term_step.COMBINED:
            combined = self.dimermo_equation["combined_all"]
        elif evaluated == term_step.SORTED:
            combined = self.dimermo_equation["sorted_all"]
        else:  # EVALUATED
            combined = self.dimermo_equation["combined_sorted_evaluated"]
        combined, lines, latex_equation = self.get_equational_form(combined,detailed=True)
        self.latex_equation[evaluated.value] = latex_equation

    def add_monomer_sym(self, sym:str) -> None:
        """
        add a monomer symmetry; including the check that no symmetry is listed more than once
        :param sym: monomer symmetry
        :return:
        """
        self.monomer_symmetries.append(sym)
        self.monomer_symmetries = list(set(self.monomer_symmetries))


    def print(self, detailed:bool) -> str:
        """
        get information about the class as printable string
        :param detailed: level of detail in which the content is given
        :return: lines of information/equations
        """
        sign = signed_number_to_latex_number(self.sign_and_factor)
        content = "\n" + self.get_total_mo_schemata()
        # zusammenfügen des Starts (bzgl. Sortierung):
        eq = sign + r"\cdot " + self.initial_equation["formatted"] + r"\Rightarrow " +sign+ self.initial_equation["sorted_formatted"]
        eq = eq.replace(r"+\cdot", r"+")
        content += format_irred_representations( get_expression_as_latex_formula(eq, latex_equation_types.DISPLAYED) )
        # Ausgedrückt in Dimer-Orbitalen:
        content += get_expression_as_latex_formula(
            "="+sign+ format_irred_representations(self.dimermo_equation["formatted"]),# ! ab hier Vorzeichen einbezogen!
            latex_equation_types.DISPLAYED
        )
        if detailed:
            content += get_expression_as_latex_formula(
                            format_irred_representations(self.latex_equation[term_step.COMBINED.value]),
                latex_equation_types.MULTLINE
            )
            content += get_expression_as_latex_formula(
                            format_irred_representations(self.latex_equation[term_step.SORTED.value]),
                latex_equation_types.MULTLINE
            )
        if self.latex_equation[term_step.SORTED.value] != self.latex_equation[term_step.EVALUATED.value]:
            if detailed:
                content += "summarized:"#zusammengefasst
            content += get_expression_as_latex_formula(
                                            format_irred_representations(self.latex_equation[term_step.EVALUATED.value])
                                            , latex_equation_types.MULTLINE)
            content += r"\\ \\"
        elif detailed:
            content += r"(irreducible)\\ \\"# nicht kürzbar
        else:
            content += get_expression_as_latex_formula(
                format_irred_representations(self.latex_equation[term_step.SORTED.value]),
                latex_equation_types.MULTLINE
            )
        return content




if __name__ == "__main__":
    # occupied_mos = {
    #     "b1u": {MonomerPositions.left: 0, MonomerPositions.right: 0},
    #     "au": {MonomerPositions.left: 1, MonomerPositions.right: 1},
    #     "b2g": {MonomerPositions.left: 1, MonomerPositions.right: 2},
    #     "b3g": {MonomerPositions.left: 2, MonomerPositions.right: 1},
    # }
    # d = dimer_occ_state(point_group=POINTGROUP("d2h"), occupied_mos=switch_monomers(occupied_mos), sign_and_factor=2)
    # d.set_initial_equations()
    # print( d.print(detailed=True) )

    occupied_mos = {
        "a2*": {MonomerPositions.left: 1, MonomerPositions.right: 0},
        "b2*": {MonomerPositions.left: 1, MonomerPositions.right: 0},
        "a2": {MonomerPositions.left: 1, MonomerPositions.right: 2},
        "b2": {MonomerPositions.left: 1, MonomerPositions.right: 2},
    }
    d = dimer_occ_state(point_group=POINTGROUP("c2v"), occupied_mos=switch_monomers(occupied_mos), sign_and_factor=1)
    d.set_initial_equations()
    print( d.print(detailed=True) )

from collections import defaultdict
from itertools import product
from typing import List, Tuple, Dict

from latex.signed_number_to_latex_number import signed_number_to_latex_number
from symmetries.group_theory.multipling_irred import multipling_irred
from symmetries.general_functionalities.count_swaps import count_swaps


class handeling_mos(object):

    def __init__(self,point_group):
        self.point_group = point_group

    def combine_terms(self, split_factors:List[List[str]]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        ausmultiplizieren, Bilden der Produkte von irred. Darstellungen
        :param split_factors: list of 2-item lists, that represent the monomer orbitals by dimer orbitals
        :return: list of all terms (expressed as dict)
                1.) plain result
                2.) sorted result
                3.) sorted and merged/duplicates removed
        """
        # Verwende itertools.product, um alle Kombinationen der Teilterme zu bilden
        combinations = list(product(*split_factors))

        combined_terms = []
        sorted_terms = []
        for combination in combinations:
            minus_counts = sum(term.count('-') for term in combination)
            if minus_counts % 2 == 1:
                product_term = {"amount": -1}
                product_term_sorted = {"amount": -1}
            else:
                product_term = {"amount": +1}
                product_term_sorted = {"amount": +1}
            # sort irred. representations by molpro order:
            combination = [i.replace("-", "").replace("+", "") for i in
                           combination]  # ! muss von combination verschiedenen Namen haben!
            sorted_combination = [i for i in combination]  # copy
            for i in sorted_combination:
                if i not in self.point_group.choices_irreduzible_representations_molpro_ordered:
                    raise Exception(f"{i} bzw. sein Format ist keine passende irreduzible Darstellung")
            sorted_combination = sorted(sorted_combination,
                                        key=lambda x: self.point_group.choices_irreduzible_representations_molpro_ordered.index(x))
            # check sign (number of switches within order equal -> sign stays, otherwise sign gets changed):
            counted_swaps_between_lists = count_swaps(sorted_combination, combination, print_error=False)
            if counted_swaps_between_lists % 2 == 1:
                product_term_sorted["amount"] = -product_term["amount"]

            # save result:
            product_term["eq"] = " ".join(combination)
            product_term["factors"] = combination
            combined_terms.append(product_term)
            product_term_sorted["eq"] = " ".join(sorted_combination)
            product_term_sorted["factors"] = sorted_combination
            sorted_terms.append(product_term_sorted)
        return combined_terms, sorted_terms, self.resolve_duplicates(sorted_terms)



    def resolve_duplicates(self, terms:List[Dict]) -> List[Dict]:
        """
        Kontrolle, ob gleiche Summanden vorkommen; ggf. zusammenfassen der Terme
        :param terms: summand terms, including their determinant composition, their amount and sign
        :return: summands of the equation, where duplicates are merged
        """
        # zählen:
        term_map = defaultdict(int)  # Startwert 0 für alle möglichen ergänzbaren Terme "eq"
        for term in terms:
            term_map[term["eq"]] += term['amount']

        # filtern:
        result = []
        already_added = []
        for i in terms:
            if term_map[i["eq"]] != 0 and i["eq"] not in already_added:
                amount = term_map[i["eq"]]
                if amount != 0:
                    result.append({
                        'factors': i["factors"],
                        "amount": amount,
                        "eq": i["eq"]
                    })
                    already_added.append(i["eq"])
        return result


    def get_equational_form(self, combined: List[Dict], detailed:bool=False) -> Tuple[List[Dict],str,str]:
        """
        forming equational forms of the list of terms (determinants)
        :param combined: list of the summed determinants as dict (including: amount, factors, forbidden)
        :param detailed: whether the output (latex equation) should include some details about the calculation steps
        :return:
                combined: list of the summed determinants as dict (including: amount, factors, forbidden)
                lines: result split up in multiple lines, one line per each summand, e.g. "+ag b3u b2u b1g	=		+ag\n"...
                latex_equation: latex formatted equation of the to-be-added determinants
        """
        ##### Doppelbesetzungen rausfiltern: die hier betrachteten Elektronen haben alle z.B. alpha-Spin -> kann nur 1x in gl. Orbital vorkommen
        something_relevant_included = False
        for i in range(len(combined)):
            if len(set(combined[i]["factors"])) != len(combined[i]["factors"]):
                combined[i]["forbidden"] = True
            else:
                combined[i]["forbidden"] = False
                something_relevant_included = True
        if not something_relevant_included:
            return combined, "", ""

        ##### Punktgruppe einsetzen  ##########
        latex_equation_1 = "\n="
        lines = ""
        counter = 0
        for sum in combined:
            if not sum["forbidden"]:
                lines += f'{self.get_sign_and_prefactor(sum)}{sum["eq"]}\t=\t\t'
                multipling_irred(sum,point_group=self.point_group)
                lines += f'{self.get_sign_and_prefactor(sum)}{sum["factors"][0]}\n'
                latex_equation_1 += self.get_sign_and_prefactor(sum) + r"\left|\underbrace{"
                # if detailed:
                #     latex_equation_1 += r"\overbrace{"
                latex_equation_1 += sum["eq"]
                # if detailed:
                #     latex_equation_1 += "}^{"+ irred_back_to_number(point_group=self.point_group, string=sum["eq"]).replace("*", "^*") + r"}"
                latex_equation_1 += r"}_{" + sum["factors"][0] + r"}\right|"
                counter += 1
                if counter >= 4 and sum != combined[-1]:
                    latex_equation_1 += r"\\" + "\n"
                    counter = 0
        if latex_equation_1[-1] != "\n":  # Sicherstellen, dass nur 1 Zeilenumbruch
            latex_equation_1 += "\n"
        latex_equation = latex_equation_1
        return combined, lines, latex_equation


    def get_sign_and_prefactor(self, dict_item:dict) -> str:
        return signed_number_to_latex_number(dict_item["amount"])



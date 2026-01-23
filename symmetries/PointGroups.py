from enum import Enum

from symmetries.c2h_product import c2h_product
from symmetries.c2v_product import c2v_product
from symmetries.d2h_product import d2h_product


class POINTGROUP(Enum):
    D2h = "d2h"
    C2v = "c2v"
    C2h = "c2h"


    def __new__(cls, value):
        """
        extend set-up of object by GIVEN DATA
        :param value: enum classification string
        """
        obj = object.__new__(cls)
        obj._value_ = value
        if value == "d2h":
            obj.total_symmetric = "ag"
            obj.choices_irreduzible_representations_molpro_ordered = ('ag', 'b3u', 'b2u', 'b1g', 'b1u', 'b2g', 'b3g', 'au')
            obj.choices_irreduzible_representations_molpro_ordered_monomer = ('ag', 'b3u', 'b2u', 'b1g', 'b1u', 'b2g', 'b3g', 'au')
            obj.mo_pairs = {  # !sortiert; ! brauchen Vorzeichen
                "au^{l}": "+b1g+au",
                "b1u^{l}": "+ag+b1u",
                "b2g^{l}": "+b3u+b2g",
                "b3g^{l}": "+b2u+b3g",
                "au^{r}": "-b1g+au",
                "b1u^{r}": "-ag+b1u",
                "b2g^{r}": "-b3u+b2g",
                "b3g^{r}": "-b2u+b3g"
            }
            obj.label = {"oben_links": "b1u", "oben_rechts": "au", "unten_links": "b2g", "unten_rechts": "b3g"}
        elif value == "c2v":
            obj.total_symmetric = "a1"
            obj.choices_irreduzible_representations_molpro_ordered = ('a1', 'a1*', 'b1', 'b1*', 'b2', 'b2*', 'a2', 'a2*')
            obj.choices_irreduzible_representations_molpro_ordered_monomer = ('a1', 'a1*', 'b1', 'b1*', 'b2', 'b2*', 'a2', 'a2*')
            obj.mo_pairs = {  # !sortiert; ! brauchen Vorzeichen
                "a2*^{l}":  "+b1*+a2*",#*
                "b2*^{l}":  "+a1*+b2*",#*
                "a2^{l}":   "+b1+a2",
                "b2^{l}":   "+a1+b2",
                "a2*^{r}":  "-b1*+a2*",#*
                "b2*^{r}":  "-a1*+b2*",#*
                "a2^{r}":   "-b1+a2",
                "b2^{r}":   "-a1+b2"
            }
            obj.label = {"oben_links": "b2*", "oben_rechts": "a2*", "unten_links": "a2", "unten_rechts": "b2"}
        elif value == "c2h":
            obj.total_symmetric = "ag"
            obj.choices_irreduzible_representations_molpro_ordered = ('ag', 'ag*', 'bg', 'bg*', 'bu', 'bu*', 'au', 'au*')#Dimer
            obj.choices_irreduzible_representations_molpro_ordered_monomer = ('a1', 'a1*', 'b1', 'b1*', 'b2', 'b2*', 'a2', 'a2*')#Monomer
            obj.mo_pairs = {  # !sortiert; ! brauchen Vorzeichen
                "a2*^{l}":  "+au*+bg*",#*
                "b2*^{l}":  "+ag*+bu*",#*
                "a2^{l}":   "+au+bg",
                "b2^{l}":   "+ag+bu",
                "a2*^{r}":  "+au*-bg*",#*
                "b2*^{r}":  "-ag*+bu*",#*
                "a2^{r}":   "+au-bg",
                "b2^{r}":   "-ag+bu"
            }
            obj.label = {"oben_links": "b2*", "oben_rechts": "a2*", "unten_links": "a2", "unten_rechts": "b2"}
        else:
            raise Exception("No class logic for this point group.")
        return obj

    def product(self,factor_1:str, factor_2:str):
        factor_1 = factor_1.lower()
        factor_2 = factor_2.lower()
        if self.value == "d2h":
            if (factor_1 not in self.choices_irreduzible_representations_molpro_ordered or
                    factor_2 not in self.choices_irreduzible_representations_molpro_ordered):
                raise Exception("wrong symmetry label for D2h")
            return d2h_product(factor_1=factor_1, factor_2=factor_2)
        if self.value == "c2h":
            factor_1 = factor_1.replace("*", "")
            factor_2 = factor_2.replace("*", "")
            if (factor_1 not in self.choices_irreduzible_representations_molpro_ordered or
                    factor_2 not in self.choices_irreduzible_representations_molpro_ordered):
                if factor_1 not in self.choices_irreduzible_representations_molpro_ordered_monomer or factor_2 not in self.choices_irreduzible_representations_molpro_ordered_monomer:
                    raise Exception(f"wrong symmetry label for C2h: {factor_1}, {factor_2}")
                return c2v_product(factor_1=factor_1, factor_2=factor_2)
            return c2h_product(factor_1=factor_1, factor_2=factor_2)
        if self.value == "c2v":
            factor_1 = factor_1.replace("*", "")
            factor_2 = factor_2.replace("*", "")
            if (factor_1 not in self.choices_irreduzible_representations_molpro_ordered or
                    factor_2 not in self.choices_irreduzible_representations_molpro_ordered):
                raise Exception(f"wrong symmetry label for C2v: {factor_1}, {factor_2}")
            return c2v_product(factor_1=factor_1, factor_2=factor_2)

        raise Exception("unknown point group")


if __name__ == '__main__':
    x = POINTGROUP("d2h")
    print(x)
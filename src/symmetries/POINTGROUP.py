from enum import Enum

from src.symmetries.c2h_product import c2h_product
from src.symmetries.c2v_product import c2v_product
from src.symmetries.d2h_product import d2h_product


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
            obj.irreduzible_representations_molpro_ordered = ('ag', 'b3u', 'b2u', 'b1g', 'b1u', 'b2g', 'b3g', 'au')
            obj.mo_pairs = {  # !sortiert; ! brauchen Vorzeichen
                "au^{l}" : "+b1g+au" ,
                "b1u^{l}": "+ag+b1u" ,
                "b2g^{l}": "+b3u+b2g",
                "b3g^{l}": "+b2u+b3g",
                "au^{r}" : "-b1g+au" ,
                "b1u^{r}": "-ag+b1u" ,
                "b2g^{r}": "-b3u+b2g",
                "b3g^{r}": "-b2u+b3g"
            }
            obj.label_ordering_in_monomer_occupation = {"left_top": "b1u", "right_top": "au", "left_bottom": "b2g", "right_bottom": "b3g"}
            obj.product = d2h_product
        elif value == "c2v":
            obj.total_symmetric = "a1"
            obj.irreduzible_representations_molpro_ordered = ('a1', 'a1*', 'b1', 'b1*', 'b2', 'b2*', 'a2', 'a2*')
            # INFO only * as additive marker allowed!
            #       (otherwise e.g. sorting fails, because occurence of "a1*" can be taken to be the index for "a1" in a search)
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
            obj.label_ordering_in_monomer_occupation = {"left_top": "b2*", "right_top": "a2*", "left_bottom": "a2", "right_bottom": "b2"}
            obj.product = c2v_product
        elif value == "c2h":
            obj.total_symmetric = "ag"
            obj.irreduzible_representations_molpro_ordered = ("ag", "ag*", "au", "au*", "bu", "bu*", "bg", "bg*")#'ag', 'ag*', 'bg', 'bg*', 'bu', 'bu*', 'au', 'au*')#Dimer
            # INFO only * as additive marker allowed!
            #       (otherwise e.g. sorting fails, because occurence of "a1*" can be taken to be the index for "a1" in a search)
            obj.mo_pairs = {  # !sortiert; ! brauchen Vorzeichen
                # C2v   :    C2h
                "a2*^{l}":  "+au*+bg*",#*
                "b2*^{l}":  "+ag*+bu*",#*
                "a2^{l}":   "+au+bg",
                "b2^{l}":   "+ag+bu",
                "a2*^{r}":  "+au*-bg*",#*
                "b2*^{r}":  "-ag*+bu*",#*
                "a2^{r}":   "+au-bg",
                "b2^{r}":   "-ag+bu"
            }
            obj.label_ordering_in_monomer_occupation = {"left_top": "b2*", "right_top": "a2*", "left_bottom": "a2", "right_bottom": "b2"}
            obj.product = c2h_product
        else:
            raise Exception("No class logic for this point group.")
        return obj



if __name__ == '__main__':
    x = POINTGROUP("d2h")
    print(x)
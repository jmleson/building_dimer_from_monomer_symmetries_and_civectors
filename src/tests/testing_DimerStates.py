import re
import unittest
from typing import Tuple

from src import DimerState
from src.CI_ORDERING import CI_ORDERING
from src.DimerOccupation import DimerOccupation
from src.Molecule import Molecule
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerStates(unittest.TestCase):

    def test_generation(self):
        dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6, ordering=CI_ORDERING.molpro)
        assert len(dimer_states) == 18
        strings = [d.get_label() for d in dimer_states]
        assert "S * Q + Q * S" in strings
        assert "S * Q - Q * S" in strings
        assert "i^3 b_{2u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * e^3 b_{2u} + e^3 b_{2u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * e^3 b_{2u} - e^3 b_{2u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * e^3 b_{3u} + e^3 b_{3u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * e^3 b_{3u} - e^3 b_{3u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * i^3 b_{3u} + i^3 b_{3u} * i^3 b_{2u}" in strings
        assert "i^3 b_{2u} * i^3 b_{3u} - i^3 b_{3u} * i^3 b_{2u}" in strings
        assert "e^3 b_{2u} * e^3 b_{2u}" in strings
        assert "e^3 b_{2u} * e^3 b_{3u} + e^3 b_{3u} * e^3 b_{2u}" in strings
        assert "e^3 b_{2u} * e^3 b_{3u} - e^3 b_{3u} * e^3 b_{2u}" in strings
        assert "e^3 b_{2u} * i^3 b_{3u} + i^3 b_{3u} * e^3 b_{2u}" in strings
        assert "e^3 b_{2u} * i^3 b_{3u} - i^3 b_{3u} * e^3 b_{2u}" in strings
        assert "e^3 b_{3u} * e^3 b_{3u}" in strings
        assert "e^3 b_{3u} * i^3 b_{3u} + i^3 b_{3u} * e^3 b_{3u}" in strings
        assert "e^3 b_{3u} * i^3 b_{3u} - i^3 b_{3u} * e^3 b_{3u}" in strings
        assert "i^3 b_{3u} * i^3 b_{3u}" in strings

        assert "i^3 b_{2u} * i^3 b_{2u}" == strings[2]
        d_triplet_1 = dimer_states[2]
        d_triplet_1.get_product_terms()
        assert len(d_triplet_1.dimer_occupations) == 4
        signs = [d.sign for d in d_triplet_1.dimer_occupations]
        assert signs.count(SIGN.PLUS) == 2


        # assert "i^3 b_{2u} * e^3 b_{2u} + e^3 b_{2u} * i^3 b_{2u}"  == strings[3]
        # d_triplet_2 = dimer_states[3]
        # d_triplet_2.get_product_terms()
        # assert len(d_triplet_2.dimer_occupations) == 8


    def test_multiply_out(self):
        p = POINTGROUP("d2h")

        s = MonomerOccupation(point_group=p)
        s.set_occupation({"b1u": 0, "b2g": 2, "b3g": 2, "au": 0})

        q = MonomerOccupation(point_group=p)
        q.set_occupation({"b1u": 1, "b2g": 1, "b3g": 1, "au": 1})

        d = DimerOccupation(monomer_occupation_1=s, monomer_occupation_2=q, sign=SIGN.PLUS, point_group=p)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 4*4

        strings = [det.determinants_string() for det in d.determinants]
        assert r"+ \left| \underbrace{ a_{g}b_{3u}b_{2u}b_{1g} }_{a_{g}}\right|" in strings

    def flip_sign_variants(self, variants: list[str]) -> list[str]:
        flipped = []
        for v in variants:
            if v.startswith("+"):
                flipped.append("-" + v[1:])
            elif v.startswith("-"):
                flipped.append("+" + v[1:])
            else:
                raise ValueError(f"Variant has no leading sign: {v}")
        return flipped


    def find_dimer_state_by_label_and_set_up_for_testing(self, dimer_states:list[DimerState], label:str) -> Tuple[DimerState, list[str]]:
        for i in dimer_states:
            if i.get_label() == label:
                i.get_product_terms()
                i.get_determinants()
                i.sum_up_determinants()

                ci_vectors = [i.latex_ci_equation(short_version=True) for i in i.summed_up_list_of_determinants_ci]
                simplified_ci_vectors = [
                    ('+' if '+' in i else '-') + re.search(r'\\left\|(.*?)\\right\|', i).group(1)
                    for i in ci_vectors
                ]
                return i, simplified_ci_vectors
        raise Exception(f"Dimer State {label} not to be found!")


    def test_end_results(self):
        dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6, ordering=CI_ORDERING.molpro)

        sq_plus, simplified_ci_vectors = self.find_dimer_state_by_label_and_set_up_for_testing(dimer_states=dimer_states, label="S * Q + Q * S")
        assert "+a22a0aa0" in simplified_ci_vectors
        assert "+aaaa0220" in simplified_ci_vectors
        assert "+0aa0a22a" in simplified_ci_vectors
        assert "+0220aaaa" in simplified_ci_vectors
        assert "+aa2002aa" in simplified_ci_vectors
        assert "-a2a00a2a" in simplified_ci_vectors
        assert "-0a2aa2a0" in simplified_ci_vectors
        assert "+02aaaa20" in simplified_ci_vectors


        sq_minus, simplified_ci_vectors = self.find_dimer_state_by_label_and_set_up_for_testing(dimer_states=dimer_states, label="S * Q - Q * S")
        variants_according_to_molpro = [
            "+a2aa0a20",
            "-aa2a02a0",
            "-0a20a2aa",
            "+02a0aa2a",
            "+a2200aaa",
            "+aaa0022a",
            "-0aaaa220",
            "-022aaaa0",
        ]
        sign_switched_variants = self.flip_sign_variants(variants_according_to_molpro)#INFO since negative LC can be build two ways -> sign switch possible (however if switch it has to be for all vectors)
        all_molpro = all(v in simplified_ci_vectors for v in variants_according_to_molpro)
        all_sign_switched = all(v in simplified_ci_vectors for v in sign_switched_variants)
        assert all_molpro or all_sign_switched, "Sign inconsistency / wrong ci vectors"


        root1, simplified_ci_vectors = self.find_dimer_state_by_label_and_set_up_for_testing(dimer_states, label ="i^3 b_{2u} * i^3 b_{2u}")
        assert len(simplified_ci_vectors) == 10
        assert root1.symmetry == "ag"
        variants_according_to_molpro = [
                "+a2a0a2a0",
                "+0a2a0a2a",
                "-a22a0aa0",
                "+aaaa0220",
                "-0aa0a22a",
                "+0220aaaa",
                "-aa2002aa",
                "-a2a00a2a",
                "-0a2aa2a0",
                "-02aaaa20"
        ]
        all_molpro = all(v in simplified_ci_vectors for v in variants_according_to_molpro)
        assert all_molpro, " wrong ci vectors"

        root2, simplified_ci_vectors = self.find_dimer_state_by_label_and_set_up_for_testing(dimer_states,
                                                       label="i^3 b_{2u} * e^3 b_{2u} + e^3 b_{2u} * i^3 b_{2u}")
        assert len(simplified_ci_vectors) == 2
        assert root1.symmetry == "ag"



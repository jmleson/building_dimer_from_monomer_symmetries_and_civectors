import unittest

from src.symmetries.CI_ORDERING import CI_ORDERING
from src.building_blocks.DimerOccupation import DimerOccupation
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics_and_combinations.Sign import SIGN
from src.mathematics_and_combinations.get_all_combinations import get_all_combinations
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerOccupation(unittest.TestCase):

    point_group = POINTGROUP.D2h




    def test_get_all_combinations(self):
        a1 = {"sym_label": "a", "sign": "+", "paired_label": "b", "occupation": 1}
        b1 = {"sym_label": "b", "sign": "+", "paired_label": "a", "occupation": 1}
        possibilities_1 = [ a1, b1 ]
        a2 = {"sym_label": "a", "sign": "-", "paired_label": "b", "occupation": 0}
        b2 = {"sym_label": "b", "sign": "-", "paired_label": "a", "occupation": 0}
        possibilities_2 = [ a2, b2 ]
        combo = get_all_combinations(possibilities_1, possibilities_2)

        assert len(combo) == 2
        assert (a1, b2) in combo
        assert (a2, b1) in combo

    def test_get_determinants(self):
        # 0 orbitals different:
        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        d1 = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d1.multiply_out(ordering=CI_ORDERING.molpro)

        d1_minus = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.MINUS)
        d1_minus.multiply_out(ordering=CI_ORDERING.molpro)

        assert len(d1.determinants) == 1
        assert (r"+\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{a_{g}}\right|" == d1.determinants[0].latex_ci_equation())

        assert len(d1_minus.determinants) == 1
        assert (r"-\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{a_{g}}\right|" == d1_minus.determinants[0].latex_ci_equation())

        assert d1.determinants[0].sign == SIGN.PLUS
        assert d1_minus.determinants[0].sign == SIGN.MINUS

        # 2 orbitals different:
        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 0, "au": 1})

        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering = CI_ORDERING.molpro)
        assert len(d.determinants) == 2**2
        strings = [i.latex_ci_equation() for i in d.determinants]
        assert (r"+\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{0}(b2g)^{2}(b3g)^{1}(au)^{1}")
                + r"}_{b_{1g}}\right|" in strings )
        assert (r"-\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{1}(b1u)^{0}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{a_{u}}\right|" in strings )
        assert (r"+\left|\underbrace{"+
                format_irred_representations("(ag)^{0}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{1}")
                + r"}_{a_{u}}\right|" in strings )
        # assert (r"-\left|\underbrace{"+
        #         format_irred_representations("(ag)^{0}(b3u)^{2}(b2u)^{1}(b1g)^{1}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
        #         + r"}_{b_{1g}}\right|" in strings )


        # 3 orbitals different:
        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 1, "b3g": 1, "b1u": 0, "au": 2})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2**3

        # 4 orbitals different:
        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 1, "b3g": 2, "b1u": 0, "au": 1})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2**4


        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 1, "b3g": 2, "b1u": 0, "au": 1})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2 ** 4

    def test_added_test_for_get_determinants_C6H6(self):
        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 1
        assert d.determinants[0].sign == SIGN.PLUS

        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 1, "b3g": 2, "b1u": 0, "au": 1})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        d_minus = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.MINUS)# changed sign of DimerOccupation only -> should give inverted result:
        d_minus.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2 ** 4
        assert len(d_minus.determinants) == 2 ** 4


        condition1 = r"(+a_{g}+b_{1u})^{0}(+b_{3u}+b_{2g})^{1}(+b_{2u}+b_{3g})^{2}(+b_{1g}+a_{u})^{1}" in d.written_in_monomer_ci_vectors(ordering=CI_ORDERING.molpro, multiplied_out=True)
        condition2 = r"(-a_{g}+b_{1u})^{1}(-b_{3u}+b_{2g})^{2}(-b_{2u}+b_{3g})^{1}(-b_{1g}+a_{u})^{0}" in d.written_in_monomer_ci_vectors(ordering=CI_ORDERING.molpro, multiplied_out=True)
        condition1_minus = r"(+a_{g}+b_{1u})^{0}(+b_{3u}+b_{2g})^{1}(+b_{2u}+b_{3g})^{2}(+b_{1g}+a_{u})^{1}" in d_minus.written_in_monomer_ci_vectors(ordering=CI_ORDERING.molpro, multiplied_out=True)
        condition2_minus = r"(-a_{g}+b_{1u})^{1}(-b_{3u}+b_{2g})^{2}(-b_{2u}+b_{3g})^{1}(-b_{1g}+a_{u})^{0}" in d_minus.written_in_monomer_ci_vectors(ordering=CI_ORDERING.molpro, multiplied_out=True)

        condition3 = "(a_{g})^{0}(b_{3u})^{1}(b_{2u})^{2}(b_{1g})^{1}(b_{1u})^{1}(b_{2g})^{2}(b_{3g})^{1}(a_{u})^{0}" in d.determinants[0].latex_ci_equation()
        condition3_minus = "(a_{g})^{0}(b_{3u})^{1}(b_{2u})^{2}(b_{1g})^{1}(b_{1u})^{1}(b_{2g})^{2}(b_{3g})^{1}(a_{u})^{0}" in d_minus.determinants[0].latex_ci_equation()
        # order now: b3u b1g b1u b3g    -> before (s. conditions 1 & 2):   +b3u  +b1g   +b1u   +b3g
        if condition1 and condition2 and condition3 and condition1_minus and condition2_minus and condition3_minus:
            assert d.determinants[0].sign == SIGN.PLUS # 0 swaps
            assert d_minus.determinants[0].sign == SIGN.MINUS  # 0 swaps
        else:
            raise Warning("! Attention, this test is meant to run")

        condition3 = "(a_{g})^{0}(b_{3u})^{1}(b_{2u})^{2}(b_{1g})^{0}(b_{1u})^{1}(b_{2g})^{2}(b_{3g})^{1}(a_{u})^{1}" in d.determinants[1].latex_ci_equation()
        # order now: b3u  b1u  b3g  au      -> before (s. conditions 1 & 2):    +b3u   +au   +b1u     +b3g
        if condition1 and condition2 and condition3 and condition1_minus and condition2_minus and condition3_minus:
            assert d.determinants[0].sign == SIGN.PLUS# counted swaps = 2
            assert d_minus.determinants[0].sign == SIGN.MINUS
        else:
            raise Warning("! Attention, this test is meant to run")

        condition3 = "(a_{g})^{0}(b_{3u})^{1}(b_{2u})^{1}(b_{1g})^{0}(b_{1u})^{1}(b_{2g})^{2}(b_{3g})^{2}(a_{u})^{1}" in d.determinants[3].latex_ci_equation()
        # order now:   b3u b2u b1u au    -> before (s. conditions 1 & 2):   +b3u  +au  +b1u  -b2u
        if condition1 and condition2 and condition3 and condition1_minus and condition2_minus and condition3_minus:
            assert d.determinants[0].sign == SIGN.PLUS  # counted swaps = 1, however one - in used orbitals
            assert d_minus.determinants[0].sign == SIGN.MINUS
        else:
            raise Warning("! Attention, this test is meant to run")


    def find_determinant_by_ci_vector(self, determinants, ci_vector_part:str):
        indices = []
        for d in range(len(determinants)):
            if ci_vector_part in determinants[d].latex_ci_equation():
                indices.append(d)
        if len(indices) == 0:
            raise Exception("! Attention, this test is meant to run")
        if len(indices) != 1:
            raise Exception(f"wth? one Dimer Occupation cannot have multiple identical ci vectors {indices}")
        return determinants[indices[0]]

    def test_added_test_for_get_determinants_C6H5Cl(self):
        p = POINTGROUP.C2v

        m1 = MonomerOccupation(point_group=p)
        m1.set_occupation({"b2": 1, "b2*": 1, "a2": 2, "a2*": 0})
        m2 = MonomerOccupation(point_group=p)
        m2.set_occupation({"b2": 2, "b2*": 1, "a2": 1, "a2*": 0})
        d = DimerOccupation(m1, m2, point_group=p, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2**2

        assert r"(+a_1+b_2)^{1}(+a_1^{*}+b_2^{*})^{1}(+b_1+a_2)^{2}(+b_1^{*}+a_2^{*})^{0}" in d.written_in_monomer_ci_vectors(
            ordering=CI_ORDERING.molpro, multiplied_out=True)
        assert r"(-a_1+b_2)^{2}(-a_1^{*}+b_2^{*})^{1}(-b_1+a_2)^{1}(-b_1^{*}+a_2^{*})^{0}" in d.written_in_monomer_ci_vectors(
            ordering=CI_ORDERING.molpro, multiplied_out=True)

        d0 = self.find_determinant_by_ci_vector(determinants=d.determinants,
              ci_vector_part="(a_1)^{1}(a_1^{*})^{1}(b_1)^{2}(b_1^{*})^{0}(b_2)^{2}(b_2^{*})^{1}(a_2)^{1}(a_2^{*})^{0}")
        # order now:   a1  a2      -> before (s. conditions 1 & 2):  a1   a2
        assert d0.sign == SIGN.PLUS  # counted swaps = 0


        d1 = self.find_determinant_by_ci_vector(determinants=d.determinants,
              ci_vector_part="(a_1)^{1}(a_1^{*})^{1}(b_1)^{1}(b_1^{*})^{0}(b_2)^{2}(b_2^{*})^{1}(a_2)^{2}(a_2^{*})^{0}")
        # order now:  a1  b1        -> before (s. conditions 1 & 2):  a1 -b1
        assert d1.sign == SIGN.MINUS  # counted swaps = 0, but 1 minus

        dx = self.find_determinant_by_ci_vector(determinants=d.determinants,
              ci_vector_part="(a_1)^{2}(a_1^{*})^{1}(b_1)^{2}(b_1^{*})^{0}(b_2)^{1}(b_2^{*})^{1}(a_2)^{1}(a_2^{*})^{0}")#21201110
        # order now:   b2  a2      -> before (s. conditions 1 & 2):  b2  a2
        assert dx.sign == SIGN.PLUS  # counted swaps = 0



        m1 = MonomerOccupation(point_group=p)
        m1.set_occupation({"b2": 2, "b2*": 1, "a2": 1, "a2*": 0})
        m2 = MonomerOccupation(point_group=p)
        m2.set_occupation({"b2": 1, "b2*": 1, "a2": 2, "a2*": 0})
        d = DimerOccupation(m1, m2, point_group=p, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2**2

        assert r"(+a_1+b_2)^{2}(+a_1^{*}+b_2^{*})^{1}(+b_1+a_2)^{1}(+b_1^{*}+a_2^{*})^{0}" in d.written_in_monomer_ci_vectors(
            ordering=CI_ORDERING.molpro, multiplied_out=True)
        assert r"(-a_1+b_2)^{1}(-a_1^{*}+b_2^{*})^{1}(-b_1+a_2)^{2}(-b_1^{*}+a_2^{*})^{0}" in d.written_in_monomer_ci_vectors(
            ordering=CI_ORDERING.molpro, multiplied_out=True)

        dx = self.find_determinant_by_ci_vector(determinants=d.determinants,
                   ci_vector_part="(a_1)^{2}(a_1^{*})^{1}(b_1)^{2}(b_1^{*})^{0}(b_2)^{1}(b_2^{*})^{1}(a_2)^{1}(a_2^{*})^{0}")  # 21201110
        # order now:  b2   a2    -> before (s. conditions 1 & 2):  a2  b2
        assert dx.sign == SIGN.MINUS  # counted swaps = 1
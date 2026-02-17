import unittest

from src.CI_ORDERING import CI_ORDERING
from src.DimerOccupation import DimerOccupation
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics.Sign import SIGN
from src.mathematics.get_all_combinations import get_all_combinations
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerOccupation(unittest.TestCase):

    point_group = POINTGROUP.D2h

    m1 = MonomerOccupation(point_group=point_group)
    m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
    m2 = MonomerOccupation(point_group=point_group)
    m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
    d1 = DimerOccupation(m1, m2, point_group=point_group, sign=SIGN.PLUS)
    d1.multiply_out(ordering=CI_ORDERING.molpro)

    d1_minus = DimerOccupation(m1, m2, point_group=point_group, sign=SIGN.MINUS)
    d1_minus.multiply_out(ordering=CI_ORDERING.molpro)


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
        assert len(self.d1.determinants) == 1
        assert (r"+\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{a_{g}}\right|" == self.d1.determinants[0].latex_ci_equation())

        assert len(self.d1_minus.determinants) == 1
        assert (r"-\left|\underbrace{"+
                format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{a_{g}}\right|" == self.d1_minus.determinants[0].latex_ci_equation())

        assert self.d1.determinants[0].sign == SIGN.PLUS
        assert self.d1_minus.determinants[0].sign == SIGN.MINUS

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
        assert (r"-\left|\underbrace{"+
                format_irred_representations("(ag)^{0}(b3u)^{2}(b2u)^{1}(b1g)^{1}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
                + r"}_{b_{1g}}\right|" in strings )


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


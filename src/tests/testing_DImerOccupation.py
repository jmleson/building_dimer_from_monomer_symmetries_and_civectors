import unittest

from src.CI_ORDERING import CI_ORDERING
from src.DimerOccupation import DimerOccupation
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.latex.format_irred_representations import format_irred_representations
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerOccupation(unittest.TestCase):

    point_group = POINTGROUP.D2h

    def test_get_determinants(self):
        # # 0 orbitals different:
        # m1 = MonomerOccupation(point_group=self.point_group)
        # m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        # m2 = MonomerOccupation(point_group=self.point_group)
        # m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        #
        # d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        # d.multiply_out(ordering = CI_ORDERING.molpro)
        # assert len(d.determinants) == 1
        # assert (r"+\left|"+
        #         format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
        #         + r"\right|" == d.determinants[0].latex_ci_equation())
        #
        #
        # # 2 orbitals different:
        # m1 = MonomerOccupation(point_group=self.point_group)
        # m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        # m2 = MonomerOccupation(point_group=self.point_group)
        # m2.set_occupation({"b2g": 2, "b3g": 1, "b1u": 0, "au": 1})
        #
        # d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        # d.multiply_out(ordering = CI_ORDERING.molpro)
        # assert len(d.determinants) == 2**2
        # strings = [i.latex_ci_equation() for i in d.determinants]
        # assert (r"+\left|"+
        #         format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{0}(b2g)^{2}(b3g)^{1}(au)^{1}")
        #         + r"\right|" in strings )
        # assert (r"+\left|"+
        #         format_irred_representations("(ag)^{1}(b3u)^{2}(b2u)^{1}(b1g)^{1}(b1u)^{0}(b2g)^{2}(b3g)^{1}(au)^{0}")
        #         + r"\right|" in strings )
        # assert (r"+\left|"+
        #         format_irred_representations("(ag)^{0}(b3u)^{2}(b2u)^{1}(b1g)^{0}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{1}")
        #         + r"\right|" in strings )
        # assert (r"+\left|"+
        #         format_irred_representations("(ag)^{0}(b3u)^{2}(b2u)^{1}(b1g)^{1}(b1u)^{1}(b2g)^{2}(b3g)^{1}(au)^{0}")
        #         + r"\right|" in strings )
        #
        #
        # # 3 orbitals different:
        # m1 = MonomerOccupation(point_group=self.point_group)
        # m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        # m2 = MonomerOccupation(point_group=self.point_group)
        # m2.set_occupation({"b2g": 1, "b3g": 1, "b1u": 0, "au": 2})
        # d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        # d.multiply_out(ordering=CI_ORDERING.molpro)
        # assert len(d.determinants) == 2**3
        #
        # # 4 orbitals different:
        # m1 = MonomerOccupation(point_group=self.point_group)
        # m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        # m2 = MonomerOccupation(point_group=self.point_group)
        # m2.set_occupation({"b2g": 1, "b3g": 2, "b1u": 0, "au": 1})
        # d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        # d.multiply_out(ordering=CI_ORDERING.molpro)
        # assert len(d.determinants) == 2**4


        m1 = MonomerOccupation(point_group=self.point_group)
        m1.set_occupation({"b2g": 2, "b3g": 1, "b1u": 1, "au": 0})
        m2 = MonomerOccupation(point_group=self.point_group)
        m2.set_occupation({"b2g": 1, "b3g": 2, "b1u": 0, "au": 1})
        d = DimerOccupation(m1, m2, point_group=self.point_group, sign=SIGN.PLUS)
        d.multiply_out(ordering=CI_ORDERING.molpro)
        assert len(d.determinants) == 2 ** 4


import unittest

from numpy.version import short_version

from src.CI_ORDERING import CI_ORDERING
from src.building_blocks.DimerDeterminant import DimerDeterminant
from src.mathematics.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerDeterminant(unittest.TestCase):

    p = POINTGROUP.D2h

    d1 = DimerDeterminant(orbital_symmetry_labels_occ1= ["+ag", "-b1u", "+b2g", "-au"], orbital_symmetry_labels_occ0=["b1g", "b3g"],
                          sign=SIGN.PLUS, point_group=p, ordering=CI_ORDERING.molpro)
    d2 = DimerDeterminant(orbital_symmetry_labels_occ1= ["+ag", "-b1u", "+b2g", "-au"], orbital_symmetry_labels_occ0=["b1g", "b3g"],
                          sign=SIGN.MINUS, point_group=p, ordering=CI_ORDERING.molpro)
    d3 = DimerDeterminant(orbital_symmetry_labels_occ1= ["+ag", "-b1u", "+b2g", "-au"], orbital_symmetry_labels_occ0=["b3g", "b2u"],
                          sign=SIGN.MINUS, point_group=p, ordering=CI_ORDERING.molpro)

    d4 = DimerDeterminant(orbital_symmetry_labels_occ1= ["+ag", "-b1u", "+b2g", "-au"], orbital_symmetry_labels_occ0=["b3g", "b2u"],
                          sign=SIGN.PLUS, point_group=p, ordering=CI_ORDERING.molpro)

    d5 = DimerDeterminant(orbital_symmetry_labels_occ1= ["+ag", "-b1u", "+b2g", "-au"], orbital_symmetry_labels_occ0=["b3u", "b2u"],
                          sign=SIGN.PLUS, point_group=p, ordering=CI_ORDERING.molpro)



    def test_addable(self):
        assert self.d1 != self.d2
        assert self.d1.addable(self.d2, regarding="symmetry")
        assert self.d1.addable(self.d2, regarding="ci vector")

        assert self.d1.addable(self.d3, regarding="symmetry")
        assert not self.d1.addable(self.d3, regarding="ci vector") and not self.d3.addable(self.d1, regarding="ci vector")

        assert self.d3.addable(self.d4, regarding="symmetry")
        assert self.d3.addable(self.d4, regarding="ci vector")

        assert self.d3.addable(self.d5, regarding="symmetry")
        assert not self.d3.addable(self.d5, regarding="ci vector")

    def test_ci_vector(self):

        try:
            eq = self.d1.latex_ci_equation()
            raise Exception("should raise error because zero-orbitals are not set")
        except:
            pass

        try:
            eq = self.d2.latex_ci_equation()
            raise Exception("should raise error because zero-orbitals are not set")
        except:
            pass

        # INFO order = ('ag', 'b3u', 'b2u', 'b1g', 'b1u', 'b2g', 'b3g', 'au')

        eq = self.d3.latex_ci_equation(short_version=True)
        # 1e- = "+ag", "-b1u", "+b2g", "-au"], zero = ["b3g", "b2u"]
        assert eq == r"-\left|"+ "a202aa0a" + r"\right|"

        eq = self.d4.latex_ci_equation(short_version=True)
        assert eq == r"+\left|" + "a202aa0a" + r"\right|"




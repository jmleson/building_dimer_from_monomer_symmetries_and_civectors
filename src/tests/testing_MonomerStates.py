import copy
import unittest

from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.building_blocks.MonomerState import MonomerState
from src.mathematics_and_combinations.Sign import SIGN
from src.symmetries.POINTGROUP import POINTGROUP


class TestMonomerState(unittest.TestCase):


    def test_empty_monomer(self):
        p = POINTGROUP("d2h")

        m = MonomerOccupation(point_group=p)

        assert m.right_top.sym_label == "au" and m.right_top.occupation == 0
        assert m.left_top.sym_label == "b1u" and m.left_top.occupation == 0
        assert m.right_bottom.sym_label == "b3g" and m.right_bottom.occupation == 0
        assert m.left_bottom.sym_label == "b2g" and m.left_bottom.occupation == 0

        s = m.latex_picture(draw_label=False)
        s = s.replace(" ", "").replace("\t", "").replace("\n", "").replace("%lowerMOs:", "").replace("%upperMOs:", "")
        assert s == r"\draw[thick](0,-0.6)--(0.5,-0.6)%node[pos=0,left]{$b_{2g}$};;\draw[thick](1,-0.6)--(1.5,-0.6)%node[pos=1,right]{$b_{3g}$};;\draw[thick](0,0)--(0.5,0)%node[pos=0,left]{$b_{1u}$};;\draw[thick](1,0)--(1.5,0)%node[pos=1,right]{$a_{u}$};;"
        s = [i for i in s.split(";") if len(i) > 0]
        assert len(s) == 4


        s = m.latex_picture(draw_label=True)
        s = s.replace(" ", "").replace("\t", "").replace("\n", "").replace("%lowerMOs:", "").replace("%upperMOs:", "")
        assert s == r"\draw[thick](0,-0.6)--(0.5,-0.6)node[pos=0,left]{$b_{2g}$};;\draw[thick](1,-0.6)--(1.5,-0.6)node[pos=1,right]{$b_{3g}$};;\draw[thick](0,0)--(0.5,0)node[pos=0,left]{$b_{1u}$};;\draw[thick](1,0)--(1.5,0)node[pos=1,right]{$a_{u}$};;"
        s = [i for i in s.split(";") if len(i) > 0]
        assert len(s) == 4


    def test_MonomerState(self):
        p = POINTGROUP("d2h")

        m1 = MonomerOccupation(point_group=p)
        m1.set_occupation({"b1u": 1, "b2g": 2, "b3g": 1, "au": 0})
        assert m1.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) == r"\left|a2a0\right|"

        m2 = MonomerOccupation(point_group=p)
        m2.set_occupation({"b1u": 0, "b2g": 1, "b3g": 2, "au": 1})
        assert m2.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) == r"\left|0a2a\right|"

        ms1 = MonomerState(label="i^3 B_{2u}", point_group=p, molpro_symmetry_number= 3)
        ms1.set_monomer_occupations(always_positive_monomer_occupation=m1, additive_monomer_occupation=m2, combination=SIGN.MINUS)
        ms1.latex_picture(draw_label=False)
        assert ms1.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) == r"\left|a2a0\right| - \left|0a2a\right|"
        assert ms1.get_multiplicity() == 3

        ms2 = MonomerState(label="i^3 B_{2u}", point_group=p, molpro_symmetry_number=3)
        ms2.set_monomer_occupations(always_positive_monomer_occupation=m1, additive_monomer_occupation=m2,
                                  combination=SIGN.PLUS)
        assert ms2.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) == r"\left|a2a0\right| + \left|0a2a\right|"
        assert ms2.get_multiplicity() == 3

        assert ms1 == copy.deepcopy(ms1)
        assert ms1 != ms2


    def test_getting_monomer_states(self):
        triplets = Molecule.C6H6.get_ci_vectors_triplets()
        strings = [t.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) for t in triplets]
        assert len(strings) == 6
        assert r"\left|aaaa\right|" in strings
        assert r"\left|0220\right|" in strings
        assert r"\left|a2a0\right| - \left|0a2a\right|" in strings
        assert r"\left|a2a0\right| + \left|0a2a\right|" in strings
        assert r"\left|aa20\right| - \left|02aa\right|" in strings
        assert r"\left|aa20\right| + \left|02aa\right|" in strings
        multiplicities = [t.get_multiplicity() for t in triplets]
        assert sorted(multiplicities) == [1, 3, 3, 3, 3, 5]

        triplets_Cl = Molecule.C6H5Cl.get_ci_vectors_triplets()
        strings_Cl = [t.latex_ci_equation(ordering=CI_ORDERING.molpro, multiplied_out=False, short_version=True) for t in triplets_Cl]
        assert len(strings_Cl) == 6
        assert r"\left|aaaa\right|" in strings
        assert r"\left|0220\right|" in strings
        assert r"\left|aa20\right| - \left|20aa\right|" in strings_Cl
        assert r"\left|aa20\right| + \left|20aa\right|" in strings_Cl
        assert r"\left|2aa0\right| - \left|a02a\right|" in strings_Cl
        assert r"\left|2aa0\right| + \left|a02a\right|" in strings_Cl

        # triplets_rotated_Cl = Molecule.C6H5Cl_rotated.get_ci_vectors_triplets()
        # strings_rotated_Cl = [t.latex_ci_equation(ordering=CI_ORDERING.molpro) for t in triplets_rotated_Cl]
        # assert strings_rotated_Cl == strings_Cl





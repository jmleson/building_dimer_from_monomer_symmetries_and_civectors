import unittest

from src.CI_ORDERING import CI_ORDERING
from src.MonomerOccupation import MonomerOccupation
from src.MonomerState import MonomerState
from src.Sign import SIGN
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
        assert s == "\draw[thick](0,-0.6)--(0.5,-0.6)%node[pos=0,left]{$b_{2g}$}%;\draw[thick](1,-0.6)--(1.5,-0.6)%%node[pos=1,right]{$b_{3g}$};\draw[thick](0,0)--(0.5,0)%node[pos=0,left]{$b_{1u}$}%;\draw[thick](1,0)--(1.5,0)%%node[pos=1,right]{$a_{u}$};"
        s = [i for i in s.split(";") if len(i) > 0]
        assert len(s) == 4


        s = m.latex_picture(draw_label=True)
        s = s.replace(" ", "").replace("\t", "").replace("\n", "").replace("%lowerMOs:", "").replace("%upperMOs:", "")
        assert s == "\draw[thick](0,-0.6)--(0.5,-0.6)node[pos=0,left]{$b_{2g}$};\draw[thick](1,-0.6)--(1.5,-0.6)node[pos=1,right]{$b_{3g}$};\draw[thick](0,0)--(0.5,0)node[pos=0,left]{$b_{1u}$};\draw[thick](1,0)--(1.5,0)node[pos=1,right]{$a_{u}$};"
        s = [i for i in s.split(";") if len(i) > 0]
        assert len(s) == 4


    def test_MonomerState(self):
        p = POINTGROUP("d2h")

        m1 = MonomerOccupation(point_group=p)
        m1.set_occupation({"b1u": 1, "b2g": 2, "b3g": 1, "au": 0})
        assert m1.latex_ci_equation(order=CI_ORDERING.molpro) == r"\left|a2a0\right|"

        m2 = MonomerOccupation(point_group=p)
        m2.set_occupation({"b1u": 0, "b2g": 1, "b3g": 2, "au": 1})
        assert m2.latex_ci_equation(order=CI_ORDERING.molpro) == r"\left|0a2a\right|"

        m = MonomerState(label="i^3 b_{2u}", point_group=p, symmetry_index = 3 )
        m.set_monomer_occupations(always_positive_monomer_occupation=m1, additive_monomer_occupation=m2, combination=SIGN.MINUS)

        m.latex_picture(draw_label=False)

        assert m.latex_ci_equation(order=CI_ORDERING.molpro) == r"\left|a2a0\right| - \left|0a2a\right|"





import unittest

from src.MonomerOccupation import MonomerOccupation
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




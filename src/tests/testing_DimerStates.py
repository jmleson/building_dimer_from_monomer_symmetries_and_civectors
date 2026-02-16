import unittest

from src.DimerOccupation import DimerOccupation
from src.Molecule import Molecule
from src.building_blocks.MonomerOccupation import MonomerOccupation
from src.latex.basic_latex_header import basic_latex_header
from src.latex.latex_equation_types import get_expression_as_latex_formula, latex_equation_types
from src.latex.wrap_tikz_picture import wrap_tikz_picture
from src.mathematics.Sign import SIGN
from src.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.symmetries.POINTGROUP import POINTGROUP


class TestDimerStates(unittest.TestCase):

    def test_generation(self):
        dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6)
        assert len(dimer_states) == 18
        strings = [d.get_label() for d in dimer_states]
        # assert "S * Q + Q * S" in strings
        # assert "S * Q - Q * S" in strings
        # assert "i^3 b_{2u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * e^3 b_{2u} + e^3 b_{2u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * e^3 b_{2u} - e^3 b_{2u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * e^3 b_{3u} + e^3 b_{3u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * e^3 b_{3u} - e^3 b_{3u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * i^3 b_{3u} + i^3 b_{3u} * i^3 b_{2u}" in strings
        # assert "i^3 b_{2u} * i^3 b_{3u} - i^3 b_{3u} * i^3 b_{2u}" in strings
        # assert "e^3 b_{2u} * e^3 b_{2u}" in strings
        # assert "e^3 b_{2u} * e^3 b_{3u} + e^3 b_{3u} * e^3 b_{2u}" in strings
        # assert "e^3 b_{2u} * e^3 b_{3u} - e^3 b_{3u} * e^3 b_{2u}" in strings
        # assert "e^3 b_{2u} * i^3 b_{3u} + i^3 b_{3u} * e^3 b_{2u}" in strings
        # assert "e^3 b_{2u} * i^3 b_{3u} - i^3 b_{3u} * e^3 b_{2u}" in strings
        # assert "e^3 b_{3u} * e^3 b_{3u}" in strings
        # assert "e^3 b_{3u} * i^3 b_{3u} + i^3 b_{3u} * e^3 b_{3u}" in strings
        # assert "e^3 b_{3u} * i^3 b_{3u} - i^3 b_{3u} * e^3 b_{3u}" in strings
        # assert "i^3 b_{3u} * i^3 b_{3u}" in strings

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
        d.multiply_out()
        assert len(d.determinants) == 4*4

        strings = [det.determinants_string() for det in d.determinants]
        assert r"+1 \cdot{} \left| \underbrace{ a_{g}b_{3u}b_{2u}b_{1g} }_{a_{g}}\right|" in strings



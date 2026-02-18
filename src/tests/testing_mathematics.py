import unittest

from src.mathematics_and_combinations.Sign import SIGN, build_product_from_signs_in_str


class TestMathematics(unittest.TestCase):


    def test_sign(self):
        s_plus = SIGN.PLUS
        assert s_plus.value == "+"

        s_minus = SIGN.MINUS
        assert s_minus.value == "-"

        adding = SIGN.PLUS if s_plus == s_minus else SIGN.MINUS
        assert adding.value == "-"
        adding = SIGN.PLUS if s_plus == SIGN.PLUS else SIGN.MINUS
        assert adding.value == "+"
        adding = SIGN.PLUS if s_minus == SIGN.MINUS else SIGN.MINUS
        assert adding.value == "+"


    def test_build_product_from_signs_in_str(self):
        # 0 -
        s = '+ag+b3u+b2u+b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.PLUS

        # 1 -
        s = '+ag+b3u+b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '+ag+b3u-b2u+b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '+ag-b3u+b2u+b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '-ag+b3u+b2u+b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        # 2 -
        s = '+ag+b3u-b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.PLUS

        s = '+ag-b3u+b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.PLUS

        s = '-ag+b3u-b2u+b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.PLUS

        # 3 -
        s = '+ag-b3u-b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '-ag+b3u-b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '-ag-b3u+b2u-b1g'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS

        s = '-ag-b3u-b2u+au'
        sign = build_product_from_signs_in_str(s)
        assert sign == SIGN.MINUS


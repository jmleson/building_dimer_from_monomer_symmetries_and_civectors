import unittest

from CI_Vectors.get_possible_dimer_ci import find_choices_in_monomer_ci, get_possible_dimer_ci


class TestFindChoicesInMonomerCI(unittest.TestCase):

    def test_find_choices_in_monomer_ci(self):
        left = "a2a0"
        result = find_choices_in_monomer_ci(left, left)
        assert  result == [("a", "a"), ("2", "2"), ("a", "a"), ("0", "0")]

        right = "2200"
        result = find_choices_in_monomer_ci(right, right)
        assert result == [("2", "2"), ("2", "2"), ("0", "0"), ("0", "0")]

        result = find_choices_in_monomer_ci(left, right)
        assert result == [("a", "2"), ("2", "2"), ("a", "0"), ("0", "0")]

        right = "a2aa"
        result = find_choices_in_monomer_ci(left, right)
        assert result == [("a", "a"), ("2", "2"), ("a", "a"), ("0", "a")]


    def test_get_possible_dimer_ci(self):
        left = "a2a0"
        right = "a2aa"
        result = get_possible_dimer_ci(left, right)
        assert len(result) == 2
        assert "a2a0"+"a2aa" == result[0]["sequence"]
        assert "a2aa"+"a2a0" == result[1]["sequence"]
        assert result[0]["count"] == result[1]["count"]



import unittest
from fractions import Fraction

from CI_Vectors.count import combine_sequences
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


    def test_combine_sequences(self):#TODO
        x = get_possible_dimer_ci("aa20", "a2a0")
        for i in x:
            print(i, flush=True)
        print(len(x), flush=True)
        y = get_possible_dimer_ci("a2a0", "aa20")
        for i in x:
            print(i, flush=True)
        print(len(x), flush=True)

        number_total = sum([abs(c["count"]) for c in x])
        x = [{"factor": Fraction(1, number_total) * ci["count"], "sequence": ci["sequence"]} for ci in x]
        added_up_x = combine_sequences(x)

        number_total = sum([abs(c["count"]) for c in y])
        y = [{"factor": Fraction(1, number_total) * ci["count"], "sequence": ci["sequence"]} for ci in y]
        added_up_y = combine_sequences(y)
        pass

    def test_get_possible_dimer_ci(self):
        x = get_possible_dimer_ci("a2a0", "aa20")
        y = get_possible_dimer_ci("aa20", "a2a0")

        x = sorted(x, key=lambda i: i["sequence"])
        y = sorted(y, key=lambda i: i["sequence"])
        assert x != y#TODO



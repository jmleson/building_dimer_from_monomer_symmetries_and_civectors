import copy
from typing import List


def count_swaps(list1:List, list2:List, print_error=True) -> int:
    """
    zählen der notwendigen Veratuschungen in der Reihenfolge zwischen 2 Listen
    https://blog.finxter.com/counting-swaps-5-best-ways-to-convert-one-python-list-to-another/
    :param source:
    :param target:
    :return:
    """
    # print("count_swaps", list1, list2, flush=True)
    for i in list1:
        if i not in list2:
            raise Exception("das kann auch nicht: count_swaps")
    if len(set(list1)) != len(set(list2)):
        raise Exception("wth: count_swaps")
    if list1 == list2:
        return 0
    # doppelte Werte behandeln:
    if len(list1) != len(set(list1)):
        if print_error:
            print("unable to identify number of swaps!", flush=True)
        return 0

    source = copy.deepcopy(list1)
    target = copy.deepcopy(list2)
    lookup = {val: idx for idx, val in enumerate(target)}
    source = [lookup[v] for v in source]
    swaps = 0
    for i in range(len(source)):
        while source[i] != i:
            # print(source, swaps, target)
            swap_idx = source[i]
            source[i], source[swap_idx] = source[swap_idx], source[i]
            swaps += 1
    return swaps





# testing
assert count_swaps([1,2,3], [1,2,3]) == 0
assert count_swaps([1,2,3], [1,3,2]) == 1
assert count_swaps([1,2,3], [3,1,2]) == 2

assert count_swaps(["a","b","c"], ["a","b","c"]) == 0
assert count_swaps(["a","b","c"], ["a", "c", "b"]) == 1
assert count_swaps(["a","b","c"], ["c","a", "b"]) == 2


def sort_swap_count(array_ist, array_soll):
    swaps = 0
    for i in range(len(array_ist)):
        if array_ist[i] == array_soll[i]:
            continue
        index = array_ist.index(array_soll[i], i)
        array_ist[i], array_ist[index] = array_ist[index], array_ist[i]# swap
        swaps += 1
    return swaps


array_soll = [0, 1, 2, 3]
assert sort_swap_count(array_ist=[1, 2, 0, 3], array_soll=array_soll) == 2
assert sort_swap_count([3, 0, 2, 1], array_soll) == 2
assert sort_swap_count([3, 0, 1, 2], array_soll) == 3

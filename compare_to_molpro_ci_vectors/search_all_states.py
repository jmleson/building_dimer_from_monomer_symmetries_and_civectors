from compare_to_molpro_ci_vectors.find_roots_3_and_4 import find_dimer_state_by_molpro_variants


def search_all_states(dimer_states, info:list[dict]):
    """
    :param info: e.g. [{"sym": 1, "data": data_1, "number of states": 7, "root offset": 0}, ...]
    """

    for sym in info:
        for i in range(sym["number of states"]):
            d = find_dimer_state_by_molpro_variants(data=sym["data"], dimer_states=dimer_states, row_index=i)
            if len(d) == 1:
                print("\troot", sym["root offset"] + i, "==", d[0].get_label())
            elif len(d) > 1:
                print("\troot", sym["root offset"] + i, "has multiple choices")
            else:
                print("root", sym["root offset"] + i, "not determined")

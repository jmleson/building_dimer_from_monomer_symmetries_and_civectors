import copy
from collections import Counter

from src_alongLaTex.symmetries.general_functionalities.monomer_positions import MonomerPositions


def find_choices_in_monomer_ci(ci_vector_left, ci_vector_right):
    # Combining CI-Vectors to Dimer-CI-Vectors:
    mono_order = []
    for i in range(4):
        l = ci_vector_left[i]
        r = ci_vector_right[i]

        if l not in ["a", "2", "0"] or r not in ["a", "2", "0"]:
            raise Exception(f"unknown ci vector value at index {i}")
        # --- 1) Fall: Gleichheit → eindeutig ---
        # if l == r:
        #     mono_order.append(l)
        # else:
        #     # --- 2) Fall: Mehrdeutige Kombinationen ---
        mono_order.append((l, r))

    return mono_order


def get_possible_dimer_ci(ci_vector_left, ci_vector_right):
    # comparision_list = list(ci_vector_left + ci_vector_right)

    # 1. Möglichkeiten pro Index bestimmen
    mono_order = find_choices_in_monomer_ci(ci_vector_left, ci_vector_right)

    # 2. Branching zum Erzeugen aller möglichen Kombinationen
    dimer_poss = [{MonomerPositions.left: [], MonomerPositions.right: [], "sign": "+"}]  # Start mit leerer Sequenz

    for entry in mono_order:
        new_list = []
        if len(entry) == 1 or len(set(entry)) == 1:
            for seq in dimer_poss:
                seq[MonomerPositions.left].append(entry[0])
                seq[MonomerPositions.right].append(entry[0])
                seq["sign"] = "+"
                new_list.append(seq)
        else:
            a, b = entry
            for seq in dimer_poss:
                # TODO differentiate between ab and ba sorting for monomer ci vectors -> change sign accordingly
                seq_copy = copy.deepcopy(seq)
                seq[MonomerPositions.left].append(a)
                seq[MonomerPositions.right].append(b)
                seq["sign"] = "-" if seq["sign"] == "+" else "+"
                new_list.append(seq)

                seq_copy[MonomerPositions.left].append(b)
                seq_copy[MonomerPositions.right].append(a)
                seq_copy["sign"] = "+" if seq_copy["sign"] == "+" else "-"
                new_list.append(seq_copy)

        dimer_poss = new_list

    # combine to full list:
    dimer_possibilities = []
    for i in dimer_poss:
        occ_list = i[MonomerPositions.left] + i[MonomerPositions.right]
        dimer_possibilities.append(  (i["sign"], "".join(occ_list) )   )

    # count occurences:
    counts = Counter(dimer_possibilities)
    counted_dimer_possibilities = []
    for (sign, seq), count in counts.items():
        # print(seq, "→", count)
        if sign == "-":
            count = -count
        elif sign == "+":
            count = count
        else:
            raise Exception(f"unknown sign value at {(sign, seq), count}")
        counted_dimer_possibilities.append({"count": count, "sequence": seq})
    return counted_dimer_possibilities



if __name__ == "__main__":
    x = get_possible_dimer_ci("a2a0", "aa20")
    for i in x:
        print(i)
    print(len(x))

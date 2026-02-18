from itertools import product


def is_valid_combination(combo):
    if len(combo) == 0:
        return True
    by_label = {d["sym_label"]: d for d in combo}

    for d in combo:
        paired = d["paired_label"]

        if paired in by_label:
            if d["occupation"] == by_label[paired]["occupation"] or d["occupation"] + by_label[paired]["occupation"] > 4:
                return False
        else:
            raise Exception("unknown paired label")
    if not len(combo) in [4, 8,
                          2, 6# for debugging cases only
                          ]:
        raise Exception(f"invalid combination{len(combo)}")
    return True


def get_all_combinations(possibilities_1, possibilities_2):
    combined_possibilities_per_index = []
    for i in range(len(possibilities_1)):
        combined_possibilities_per_index.append(
            [possibilities_1[i], possibilities_2[i]]
        )

    all_combinations = list(product(*combined_possibilities_per_index))

    valid_combinations = [
        combo for combo in all_combinations
        if is_valid_combination(combo)
    ]
    return valid_combinations


if __name__ == "__main__":
    possibilities_1 = [
        {"sym_label": "a", "sign": "+", "paired_label": "b", "occupation": 1, "name": "1"},
        {"sym_label": "b", "sign": "-", "paired_label": "a", "occupation": 1, "name": "2"}
    ]

    possibilities_2 = [
        {"sym_label": "a", "sign": "-", "paired_label": "b", "occupation": 0, "name": "3"},
        {"sym_label": "b", "sign": "+", "paired_label": "a", "occupation": 0, "name": "4"}
    ]

    for combo in get_all_combinations(possibilities_1, possibilities_2):
        print(combo)


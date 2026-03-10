import re

from compare_to_molpro_ci_vectors.help_functions.get_molpro_state_from_molpro_output import sign_char


def real_columns(line):
    """
    Zählt Spalten nach:
    - mindestens 2 Leerzeichen Abstand
    - enthält mindestens ein nicht-leeres Symbol
    """
    # Regex: gruppiert alles, das nicht nur Leerzeichen ist, getrennt durch 2+ Leerzeichen
    columns = re.findall(r'\S(?:.*?\S)?(?=(  +)|$)', line)
    return columns



def simplify_ci_vector_lines(line:str, ci_vector_dismiss_limit:float):

    columns = [i for i in line.split("  ") if len(i.replace(" ", "")) > 0]
    number_of_states = len(columns) - 1

    new_line = ""
    for c in range(1, len(columns)):
        number = float(columns[c])
        if abs(number) > ci_vector_dismiss_limit:  # ! needs to be carefully chosen
            # in C6H5Cl molpro prints ci vectors with factor 0.12173379, that do NOT belong to the main parts according to our derivation
            # however, some parts < 0.3 need to be included
            s = sign_char(number)
            assert len(s) == 1
            new_line += f"{s}1" + "     "  # number value is of no relevance here, only sign
    if len(new_line) > 0:
        new_line = columns[0] + "     " + new_line
    # else:
    #     print("strange line", line)

    return new_line , number_of_states


def get_ci_data_blocks(file:str, ci_vector_dismiss_limit:float, path:str="./"):
    data_blocks = []

    with open(path + file) as f:
        lines = f.readlines()

    i = 0
    root_offset = 0
    while i < len(lines):
        line = lines[i]

        if " CI Coefficients of symmetry" in line:
            # Symmetrie am Zeilenende extrahieren
            sym = int(line.strip().split()[-1])
            if sym == 1:
                root_offset = 0

            i += 3  # aktuelle Zeile + 2 skip lines

            data_sym = []

            # Daten sammeln bis leere Zeile
            while i < len(lines) and lines[i].strip() != "":
                data_sym.append(lines[i].rstrip())
                i += 1

            number_of_states = []
            new_lines = []
            for j in range(len(data_sym)):
                line_j = data_sym[j]
                new_line, number_of_states_j = simplify_ci_vector_lines(line_j, ci_vector_dismiss_limit = ci_vector_dismiss_limit)
                if new_line is not None:
                    new_lines.append(new_line)
                number_of_states.append(number_of_states_j)
            data_sym = new_lines

            number_of_states = set(number_of_states)
            assert len(number_of_states) == 1

            data_blocks.append({"sym": sym, "data": "\n".join(sorted(data_sym)), "root": len(data_blocks) // 4,
                                "number of states": list(number_of_states)[0], "root offset": root_offset})
            root_offset += data_blocks[-1]["number of states"]

        i += 1

    assert len(data_blocks) == 18 * 4
    return data_blocks



def try_to_find_deviation(infos):
    from itertools import combinations

    # Paare nach Metadaten vergleichen
    for a, b in combinations(infos, 2):
        # gleiche Metadaten außer 'data'?
        keys = ["sym", "number of states", "root offset"]
        if all(a[k] == b[k] for k in keys):
            # normalisiere die Daten (Whitespace egal)
            data_a = a["data"].replace(" ", "").replace("\t", "").replace("\n", " ")
            data_b = b["data"].replace(" ", "").replace("\t", "").replace("\n", " ")

            if data_a != data_b:
                print(f"\nDifference found for sym={a['sym']}, states={a['number of states']}, offset={a['root offset']}:")
                print(a["root"], "<->", b["root"])
                # print("\t", data_a, "!=\n\t", data_b)

                data_a = data_a.split(" ")
                data_b = data_b.split(" ")
                if not len(data_a) == len(data_b):
                    print("different data lengths")
                else:
                    for i in range(len(data_a)):
                        if data_a[i] != data_b[i]:
                            print("\t", data_a[i], "!=", data_b[i])




def read_out_data_sym(molekuel:str, ci_vector_dismiss_limit:float, path:str="./"):
    list_of_z_files = list(range(200, 605, 5)) + [2000]
    files_that_are_ok = []
    for z in list_of_z_files:
        file = f"{molekuel}-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ{z}-Plots.out"
        data_blocks = get_ci_data_blocks(file=file, path=path, ci_vector_dismiss_limit=ci_vector_dismiss_limit)

        # infos schon ohne exakte Duplikate
        infos = []  # Liste der eindeutigen Blöcke

        for block in data_blocks:
            # Prüfen, ob ein Block mit denselben Keys außer 'root' schon existiert
            found = False
            for info in infos:
                # Vergleiche alle Keys außer 'root'
                if {k: v for k, v in block.items() if k != "root"} == {k: v for k, v in info.items() if k != "root"}:
                    info["root"].append(block["root"])
                    found = True
                    break
            if not found:
                block["root"] = [block["root"]]
                infos.append(block)

        # print(infos)

        if len(infos) == 4:
            files_that_are_ok.append(file)
        else:
            try_to_find_deviation(infos=infos)

    if len(files_that_are_ok) == len(list_of_z_files):
        print(f"everything fine for {molekuel}: taking one exemplary ci vector output for dimer is represenative")





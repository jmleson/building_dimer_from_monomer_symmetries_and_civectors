



def get_molpro_civector_columns(line:str):
    if "\n" in line:
        raise Exception("multiple lines!???")
    columns = [l for l in line.split("  ") if len(l) > 0]
    return columns




def parse_output_file_for_state_dependent_ci_vectors(filename):
    result = {}

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(e)
        return None

    i = 0
    while i < len(lines):
        line = lines[i].replace("\n","")

        if "Natural orbital dump for state" in line:
            state = line[line.find("Natural orbital dump for state")+len("Natural orbital dump for state"):]
            state = state[:state.find("(")].replace(" ", "")

            state_number_in_sym = state[0]
            state_symmetry = state[-1]

            i += 1

            while i < len(lines) and " Natural orbital dump for state" not in lines[i]:
                if f" CI Coefficients of symmetry {state_symmetry}" in lines[i]:
                    i += 3
                    block_of_symmetry = []
                    while len(lines[i].replace(" ", "").replace("\n","")) > 0 and not "===" in lines[i] and not "***" in lines[i]:
                        block_of_symmetry.append(get_molpro_civector_columns(lines[i].replace("\n", "")))
                        i += 1

                    result[state] = {
                        j[0].rstrip().lstrip(): j[int(state_number_in_sym)] for j in block_of_symmetry
                    }

                i += 1
        else:
            i += 1


    assert len(result) == 18
    sorted_result = dict(
        sorted(
            result.items(),
            key=lambda item: (
                int(item[0].split(".")[1]),
                int(item[0].split(".")[0])
            )
        )
    )
    return sorted_result




if __name__ == "__main__":

    molekuel="C6H5Cl"
    z = "2000"
    path = f"compare_to_molpro_ci_vectors/data_storage/"
    file = f"{molekuel}-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ{z}-Plots.out"
    d = parse_output_file_for_state_dependent_ci_vectors(path+file)


    for x in d.items():
        print(x)
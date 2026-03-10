from compare_to_molpro_ci_vectors.help_functions.check_if_dimer_state_fits_molpro_results import find_dimer_state_by_molpro_variants
from src.latex.format_irred_representations import format_irred_representations
from src.latex.get_table import get_table
from src.symmetries.POINTGROUP import POINTGROUP


def search_all_states(dimer_states, info:list[dict]):
    """
    :param info: e.g. [{"sym": 1, "data": data_1, "number of states": 7, "root offset": 0}, ...]
    """
    all_found_states = []
    for sym in info:
        for i in range(sym["number of states"]):
            d, infos = find_dimer_state_by_molpro_variants(data=sym["data"], dimer_states=dimer_states, row_index=i)
            if len(d) == 1:
                print("\troot", sym["root offset"] + i, f"({i+1}.{sym["sym"]})", "==", d[0].get_label(), "\t\t(", d[0].symmetry, ")")
                if d[0].get_label() in all_found_states:
                    print("STRANGE: State 2x occuring")
                all_found_states.append(d[0].get_label())
            elif len(d) > 1:
                print("root", sym["root offset"] + i, f"({i+1}.{sym["sym"]})", "has multiple choices!? ")
            else:
                print("root", sym["root offset"] + i, f"({i+1}.{sym["sym"]})", "not determined")
                print(infos)




def get_table_off_all_states_agreeing_with_molpro(dimer_states, point_group:POINTGROUP, info:list[dict], ci_vector_dismiss_limit:float):
    """
    :param info: e.g. [{"sym": 1, "data": data_1, "number of states": 7, "root offset": 0}, ...]
    """
    lines = ["root (no.sym) & symmetry & linear combination by monomer states"]
    for sym in info:
        for i in range(sym["number of states"]):
            d, infos = find_dimer_state_by_molpro_variants(data=sym["data"], dimer_states=dimer_states,
                                                           row_index=i, ci_vector_dismiss_limit=ci_vector_dismiss_limit)
            if len(d) == 1:
                name =  f"\troot {sym['root offset']+ i} ({i+1}.{sym['sym']})"
                lc =  d[0].get_label()
                if point_group == POINTGROUP.D2h:
                    lc_molpro_notation = lc.replace("e^3 b_{2u}", "2.3").replace("i^3 b_{2u}", "1.3").replace("e^3 b_{3u}", "1.2").replace("i^3 b_{3u}", "2.2")# case Benzene
                else:
                    lc_molpro_notation = lc.replace("e^3 a_1", "2.1").replace("i^3 a_1", "1.1").replace("e^3 b_1", "1.2").replace("i^3 b_1", "2.2")  # case C6H5Cl (rotated or not)

                symmetry = d[0].symmetry

                line = " & ".join([name, f"${format_irred_representations(symmetry)}$", f"${lc} = {lc_molpro_notation}$"])
                lines.append(line)
    s = get_table(number_of_columns=3, content_lines=lines, break_line_distance=0.1)
    # print("\n", s, "\n")
    return s



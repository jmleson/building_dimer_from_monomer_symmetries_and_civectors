from compare_to_molpro_ci_vectors.help_functions.get_table_off_all_states_agreeing_with_molpro import \
    get_table_info_all_states_agreeing_with_molpro
from compare_to_molpro_ci_vectors.help_functions.make_hashable import make_hashable
from compare_to_molpro_ci_vectors.help_functions.parse_output_file_for_state_dependent_ci_vectors import \
    parse_output_file_for_state_dependent_ci_vectors
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.latex.format_irred_representations import format_irred_representations
from src.latex.get_table import get_table
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.symmetries.POINTGROUP import POINTGROUP




def compare_different_dimers(molecule_of_theory: Molecule, molecule_of_molpro:str, ci_vector_dismiss_limit=0.2):

    dimer_states = get_dimer_states_from_monomer_states(molecule=molecule_of_theory, ordering=CI_ORDERING.molpro)
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()


    file_info = {}
    list_of_z_files = list(range(200, 605, 5)) + [2000]
    for z in list_of_z_files:
        path = f"compare_to_molpro_ci_vectors/data_storage/"
        file = f"{molecule_of_molpro}-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ{z}-Plots.out"
        info = parse_output_file_for_state_dependent_ci_vectors(path + file)
        if info is None:
            continue

        table_information = get_table_info_all_states_agreeing_with_molpro(dimer_states=dimer_states,
                                                                          point_group=POINTGROUP.D2h, silent=True,
                                                                          info=info, molecule_of_molpro=molecule_of_molpro,
                                                                          ci_vector_dismiss_limit=ci_vector_dismiss_limit)

        file_info[z] = table_information


    general_tables = {}
    for z, table in file_info.items():
        simplified_table = make_hashable(table)
        if simplified_table not in general_tables:
            general_tables[simplified_table] = {"table": table, "z": [z]}
        else:
            general_tables[simplified_table]["z"].append(z)

    if len(general_tables) == 1:
        print(f"HURRAY: only one table sufficient to describe all dimers of {molecule_of_molpro} in theory of {molecule_of_theory.name}")
    else:
        # collect differing lines
        all_tables = [value["table"] for value in general_tables.values()]
        all_keys = set().union(*[t.keys() for t in all_tables])

        differing_lines = {}

        for k in all_keys:
            entries = []
            for value in general_tables.values():
                table = value["table"]
                if k in table:
                    entries.append(table[k])
                else:
                    entries.append(None)

            if len(set(entries)) > 1:
                differing_lines[k] = entries

        print("\nDIFFERING LINES:\n")

        for k, entries in differing_lines.items():
            print(f"State {k}:")
            for (table_info, entry) in zip(general_tables.values(), entries):
                print(f"  z in {table_info['z']}: {entry}")
            print()



    tables = {}
    for key, value in general_tables.items():
        lines = ["root (no.sym) & symmetry & linear combination by monomer states"]

        root = 0
        for key, item in value["table"].items():
            line = " & ".join([ f"\troot {root} ({key[0]})", f"${format_irred_representations(key[1])}$", item ])
            lines.append(line)
            root += 1
        table = get_table(number_of_columns=3, content_lines=lines, break_line_distance=0.1)
        tables[str(value["z"])] = table
    return tables





if __name__ == '__main__':
    compare_different_dimers(Molecule.C6H6)
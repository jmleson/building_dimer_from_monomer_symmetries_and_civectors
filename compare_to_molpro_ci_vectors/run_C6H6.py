
from compare_to_molpro_ci_vectors.help_functions.search_all_states import search_all_states, \
    get_table_off_all_states_agreeing_with_molpro
from compare_to_molpro_ci_vectors.read_out_to_data_sym import read_out_data_sym
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.symmetries.POINTGROUP import POINTGROUP



dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6, ordering=CI_ORDERING.molpro)





#INFO check first whether this procedure is representative:
for molekuel in [
    "C6H6",
    "C4H4N2",
    "C6Cl6",
    #"C6F6"#TODO
                 ]:
    path = f"compare_to_molpro_ci_vectors/data_storage/"
    full_length_infos = read_out_data_sym(path=path, molekuel=molekuel, ci_vector_dismiss_limit = 0.2)#TODO check that files are consistent to eachother too!!!

    groups = {}

    for z, info in full_length_infos.items():
        key = repr(info)  # macht dict/list vergleichbar als string

        if key not in groups:
            groups[key] = {"info": info, "z": []}

        groups[key]["z"].append(z)


    tables = {}
    seen_tables = set()

    for group in groups.values():
        info = group["info"]

        try:
            table = get_table_off_all_states_agreeing_with_molpro(
                dimer_states=dimer_states,
                info=info,
                point_group=POINTGROUP.D2h,
                ci_vector_dismiss_limit=0.2
            )

            if table not in seen_tables:
                seen_tables.add(table)
                tables[" ".join(group["z"])] = table

        except Exception as e:
            # print(e)
            raise Exception("e", e)

    if len(seen_tables) == 1:
        print(f"HURRAY, one table is sufficient for all Z-files of {molekuel}")
    else:
        for key, item in tables.items():
            print()
            print(key)
            print()
            print(item)
            print()







#
# # INFO: Results from Z200, C6H6-x2:
# data_sym_1 = """
#  0 2 a a 0 2 a a      0.00000000     -0.00000022      0.00000155      0.34701928      0.35836745     -0.70190036      0.49380170
#  a a 2 0 a a 2 0     -0.00000000     -0.00000022     -0.00000155      0.34701931      0.35836748      0.70190036      0.49380166
#  a 2 a 0 a 2 a 0      0.00000000      0.48562677      0.69607076      0.35836784     -0.34702824      0.00000153      0.00000641
#  0 a 2 a 0 a 2 a      0.00000000      0.48562663     -0.69607076      0.35836794     -0.34702833     -0.00000153      0.00000641
#  a 2 2 a 0 a a 0      0.34495841     -0.24281368      0.00000005      0.35270229      0.00566973     -0.00000002     -0.24689123
#  a a a a 0 2 2 0      0.34495841      0.24281368     -0.00000005     -0.35270229     -0.00566973      0.00000002      0.24689123
#  0 a a 0 a 2 2 a      0.34495841     -0.24281368      0.00000005      0.35270229      0.00566973     -0.00000002     -0.24689123
#  0 2 2 0 a a a a      0.34495841      0.24281368     -0.00000005     -0.35270229     -0.00566973      0.00000002      0.24689123
#  a a 2 0 0 2 a a      0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
#  a 2 a 0 0 a 2 a     -0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
#  0 a 2 a a 2 a 0     -0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
#  0 2 a a a a 2 0      0.34495841     -0.24281346      0.00000005      0.00566500     -0.35269802      0.00000002      0.24689764
# """
# data_sym_4 = """
#  a a 2 0 0 a 2 a     -0.34803459     -0.34626596     -0.35274355      0.35095096
#  0 a 2 a a a 2 0     -0.34803459     -0.34626596     -0.35274355      0.35095096
#  0 a 2 a 0 2 a a      0.34803612     -0.34626598      0.35274353      0.35094945
#  0 2 a a 0 a 2 a      0.34803612     -0.34626598      0.35274353      0.35094945
#  a 2 a 0 a a 2 0      0.34803619      0.34626601     -0.35274350      0.35094939
#  a a 2 0 a 2 a 0      0.34803619      0.34626601     -0.35274350      0.35094939
#  a 2 a 0 0 2 a a     -0.34803462      0.34626603      0.35274348      0.35095093
#  0 2 a a a 2 a 0     -0.34803462      0.34626603      0.35274348      0.35095093
# """
# data_sym_5 = """
#  a 2 a a 0 a 2 0      0.34495841     -0.34803460      0.35095096
#  a a 2 a 0 2 a 0     -0.34495841     -0.34803460      0.35095096
#  0 a 2 0 a 2 a a     -0.34495841      0.34803460     -0.35095096
#  0 2 a 0 a a 2 a      0.34495841      0.34803460     -0.35095096
#  a 2 2 0 0 a a a      0.34495841      0.34803616      0.35094943
#  a a a 0 0 2 2 a      0.34495841     -0.34803616     -0.35094943
#  0 a a a a 2 2 0     -0.34495841     -0.34803616     -0.35094943
#  0 2 2 a a a a 0     -0.34495841      0.34803616      0.35094943
# """
# data_sym_8 = """
#  a a 2 a 0 a 2 0      0.34803459      0.34626185      0.35274756     -0.35095098
#  0 a 2 0 a a 2 a     -0.34803459     -0.34626185     -0.35274756      0.35095098
#  0 2 a 0 a 2 a a      0.34803462     -0.34626192     -0.35274750     -0.35095095
#  a 2 a a 0 2 a 0     -0.34803462      0.34626192      0.35274750      0.35095095
#  0 2 2 a 0 a a a     -0.34803613      0.34627009     -0.35273950     -0.35094946
#  0 a a a 0 2 2 a      0.34803613     -0.34627009      0.35273950      0.35094946
#  a a a 0 a 2 2 0     -0.34803620     -0.34627012      0.35273947     -0.35094940
#  a 2 2 0 a a a 0      0.34803620      0.34627012     -0.35273947      0.35094940
# """





#
#
# info = [
#     {"sym": 1,  "data": data_sym_1, "number of states": 7, "root offset": 0         },
#     {"sym": 4,  "data": data_sym_4, "number of states": 4, "root offset": 0+7       },
#     {"sym": 5,  "data": data_sym_5, "number of states": 3, "root offset": 0+7+4     },
#     {"sym": 8,  "data": data_sym_8, "number of states": 4, "root offset": 0+7+4+3   },
# ]
# search_all_states(dimer_states=dimer_states, info=info)


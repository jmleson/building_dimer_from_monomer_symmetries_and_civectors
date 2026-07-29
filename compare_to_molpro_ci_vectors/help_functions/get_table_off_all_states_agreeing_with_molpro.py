from compare_to_molpro_ci_vectors.help_functions.check_if_dimer_state_fits_molpro_results import \
    check_if_dimer_state_fits_molpro_results
from compare_to_molpro_ci_vectors.help_functions.parse_output_file_for_state_dependent_ci_vectors import \
    parse_output_file_for_state_dependent_ci_vectors
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.symmetries.POINTGROUP import POINTGROUP




def get_table_info_all_states_agreeing_with_molpro(dimer_states, point_group:POINTGROUP,
                                                  molecule_of_molpro:str, info:list[dict], ci_vector_dismiss_limit:float,
                                                   silent:bool=False) -> dict:
    """
    :param info: e.g. [{"sym": 1, "data": data_1, "number of states": 7, "root offset": 0}, ...]
    """
    assert len(dimer_states) == len(info)


    collected_states = {}
    for state, ci_vectors in info.items():

        variants_according_to_molpro = [ ]
        for folge, number in ci_vectors.items():

            if molecule_of_molpro == "C6H5Cl" or molecule_of_molpro == "C6H5Clrotated":
                # active orbitals = [18.1, 19.1, 20.1, 11.2, 10.2, 18.3, 19.3, 20.3, 10.4, 11.4]
                # n orbitals = 18.1, 18.3 -> indices 0 and 5
                folge = folge.replace(" ","")
                folge = "".join([folge[f] for f in range(len(folge)) if f not in [0, 5]])
            else:
                pass # all active orbitals in molpro are considered in theoretical derivation too

            if abs(float(number)) > abs(ci_vector_dismiss_limit):
                if float(number) > 0:
                    variants_according_to_molpro.append("+"+folge.replace(" ",""))
                else:
                    variants_according_to_molpro.append("-"+folge.replace(" ",""))

        if len(variants_according_to_molpro) == 0:
            raise Exception(f"the state {state} should have some ci vector parts")

        fitting_dimer_states = []
        unfitting_dimer_states = []
        for d in dimer_states:
            check, info = check_if_dimer_state_fits_molpro_results(dimer_state=d, variants_according_to_molpro=variants_according_to_molpro)
            if check:
                fitting_dimer_states.append(d)
            else:
                unfitting_dimer_states.append(info)

        if len(fitting_dimer_states) > 1:
            if not silent:
                print("strangely found more than one fitting ci vector for state", state)
        elif len(fitting_dimer_states) == 0:
            if not silent:
                print("found no ci vector for state", state)
                for info in unfitting_dimer_states:
                    print("\t", info)
        else:
            lc = fitting_dimer_states[0].get_label()
            if point_group == POINTGROUP.D2h:
                lc_molpro_notation = lc.replace("i^3 B_{2u}", "2.3").replace("i^3 B_{2u}", "1.3").replace("i^3 B_{3u}", "1.2").replace("i^3 B_{3u}", "2.2")# case Benzene
            else:
                lc_molpro_notation = lc.replace("e^3 A_1", "2.1").replace("i^3 A_1", "1.1").replace("i^3 B_1", "1.2").replace("i^3 B_{1}", "1.2").replace("i^3 B_1", "2.2").replace("i^3 B_{1}", "2.2")  # case C6H5Cl (rotated or not)

            collected_states[(state, fitting_dimer_states[0].symmetry)] = f"${lc} = {lc_molpro_notation}$"

    # assert len(collected_states) == len(dimer_states)
    return collected_states









if __name__ == "__main__":
    dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C5H5N, ordering=CI_ORDERING.molpro)
    for d in dimer_states:
        d.get_product_terms()
        d.get_determinants()
        d.sum_up_determinants()

    molekuel = "C5H5N"
    z = "2000"
    path = f"compare_to_molpro_ci_vectors/data_storage/"
    file = f"{molekuel}-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ{z}-Plots.out"
    info = parse_output_file_for_state_dependent_ci_vectors(path + file)

    table_information = get_table_info_all_states_agreeing_with_molpro(dimer_states=dimer_states, point_group=POINTGROUP.D2h,
                                                  info=info, ci_vector_dismiss_limit=0.2, molecule_of_molpro=molekuel)

    for key, value in table_information.items():
        print(key, ":")
        print("\t", value)



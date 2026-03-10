from compare_to_molpro_ci_vectors.help_functions.search_all_states import get_table_off_all_states_agreeing_with_molpro
from compare_to_molpro_ci_vectors.read_out_to_data_sym import get_ci_data_blocks
from src.building_blocks.get_dimer_states_from_monomer_states import get_dimer_states_from_monomer_states
from src.symmetries.CI_ORDERING import CI_ORDERING
from src.symmetries.Molecule import Molecule
from src.symmetries.POINTGROUP import POINTGROUP


def compare_all_states_of_dimer():
    path = "/home/judith/Schreibtisch/Promotion/Latex_Inhaltszusammenfassungen/Ausarbeitung/DATA/results/CASCI-NEVPT2/C6H5Cl/"
    file = "C6H5Cl-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ200-Plots.out"
    data_blocks = get_ci_data_blocks(file=file, path=path)

    infos = [data_blocks[i:i+4] for i in range(0, len(data_blocks), 4)]

    dimer_states = get_dimer_states_from_monomer_states(molecule=Molecule.C6H6, ordering=CI_ORDERING.molpro)

    tables = []
    for info in infos:
        table = get_table_off_all_states_agreeing_with_molpro(dimer_states=dimer_states, info=info, point_group=POINTGROUP.D2h)
        tables.append(table)


    tables = set(tables)
    print(len(tables), "tables!!!")
    for i in tables:
        print("\n\n"+i+"\n\n")



if __name__ =='__main__':
    compare_all_states_of_dimer()